# -*- coding: utf-8 -*-


import numpy as np
import tensorflow as tf
from tensorflow.python.util import nest
from seq2seq_dialog import config


class Seq2SeqModel():
    def __init__(self, sess, mode, params, word_to_idx):
        self.sess = sess
        self.mode = mode

        self.learning_rate = params.learning_rate
        self.embedding_size = params.embedding_size
        self.rnn_size = params.rnn_size
        self.num_layers = params.num_layers
        self.use_attention = params.use_attention
        self.beam_search = params.beam_search
        self.beam_size = params.beam_size
        self.max_gradient_norm = params.max_gradient_norm
        self.bidirectional_rnn = params.bidirectional_rnn

        self.word_to_idx = word_to_idx
        self.vocab_size = len(self.word_to_idx)

        # Build model.
        self.build_model()


    def _create_rnn_cell(self):

        def single_rnn_cell():
            single_cell = tf.contrib.rnn.LSTMCell(self.rnn_size)
            cell = tf.contrib.rnn.DropoutWrapper(single_cell, 
                output_keep_prob=self.keep_prob_placeholder)
            return cell

        cell = tf.contrib.rnn.MultiRNNCell([single_rnn_cell() 
            for _ in range(self.num_layers)])
        return cell


    def build_model(self):
        print("Building model... ...")
        self.encoder_inputs = tf.placeholder(tf.int32, [None, None], name="encoder_inputs")
        self.encoder_inputs_length = tf.placeholder(tf.int32, [None], name="encoder_inputs_length")

        self.batch_size = tf.placeholder(tf.int32, [], name="batch_size")
        self.keep_prob_placeholder = tf.placeholder(tf.float32, name="keep_prob_placeholder")

        self.decoder_targets = tf.placeholder(tf.int32, [None, None], name="decoder_targets")
        self.decoder_targets_length = tf.placeholder(tf.int32, [None], name="decoder_targets_length")
        #  Example.
        #  tf.sequence_mask([1, 3, 2], 5)
        #  [[True, False, False, False, False],
        #  [True, True, True, False, False],
        #  [True, True, False, False, False]]
        self.max_target_sequence_length = tf.reduce_max(self.decoder_targets_length, name="max_target_len")
        self.mask = tf.sequence_mask(self.decoder_targets_length, 
            self.max_target_sequence_length, dtype=tf.float32, name="masks")

        with tf.variable_scope("encoder"):
            emb_matrix = np.load(config.embeddings_path + ".npy")[:self.vocab_size]
            embedding = tf.get_variable("embedding", shape=emb_matrix.shape,
                initializer=tf.constant_initializer(emb_matrix), trainable=False)
            encoder_inputs_embedded = tf.nn.embedding_lookup(embedding, self.encoder_inputs)
            if not self.bidirectional_rnn:
                encoder_cell = self._create_rnn_cell()
                encoder_outputs, encoder_state = tf.nn.dynamic_rnn(encoder_cell, encoder_inputs_embedded,
                    sequence_length=self.encoder_inputs_length, dtype=tf.float32)
            else:
                encoder_cell_fw = self._create_rnn_cell()
                encoder_cell_bw = self._create_rnn_cell()
                encoder_outputs, (encoder_state_fw, encoder_state_bw) = tf.nn.bidirectional_dynamic_rnn(
                    encoder_cell_fw, encoder_cell_bw, encoder_inputs_embedded,
                    sequence_length=self.encoder_inputs_length, dtype=tf.float32)

                encoder_outputs = tf.concat(encoder_outputs, axis=2)
                encoder_state = encoder_state_fw
                
            self.sent_emb = tf.reduce_max(encoder_outputs, axis=1)

        with tf.variable_scope("decoder"):
            encoder_inputs_length = self.encoder_inputs_length
            if self.beam_search:
                # If use beam_search, need to title_batch the outputs of encoder, just copy beam_size time.
                print("Use beamsearch decoding..")
                encoder_outputs = tf.contrib.seq2seq.tile_batch(encoder_outputs, multiplier=self.beam_size)
                encoder_state = nest.map_structure(lambda s: tf.contrib.seq2seq.tile_batch(s, self.beam_size), encoder_state)
                encoder_inputs_length = tf.contrib.seq2seq.tile_batch(self.encoder_inputs_length, multiplier=self.beam_size)

            # Use attention.
            attention_mechanism = tf.contrib.seq2seq.BahdanauAttention(
                num_units=self.rnn_size, memory=encoder_outputs,
                memory_sequence_length=encoder_inputs_length)

            decoder_cell = self._create_rnn_cell()
            decoder_cell = tf.contrib.seq2seq.AttentionWrapper(
                cell=decoder_cell, attention_mechanism=attention_mechanism,
                attention_layer_size=self.rnn_size, name="Attention_Wrapper")

            batch_size = self.batch_size if not self.beam_search else self.batch_size * self.beam_size

            decoder_initial_state = decoder_cell.zero_state(
                batch_size=batch_size, dtype=tf.float32).clone(cell_state=encoder_state)
            output_layer = tf.layers.Dense(self.vocab_size, 
                kernel_initializer=tf.truncated_normal_initializer(mean=0.0, stddev=0.1))

            if self.mode == "train":
                ending = tf.strided_slice(self.decoder_targets, [0, 0], [self.batch_size, -1], [1, 1])
                decoder_input = tf.concat([tf.fill([self.batch_size, 1], self.word_to_idx["<go>"]), ending], 1)
                decoder_inputs_embedded = tf.nn.embedding_lookup(embedding, decoder_input)

                sampling_prob = tf.Variable(0.4, dtype=tf.float32)
                training_helper = tf.contrib.seq2seq.ScheduledEmbeddingTrainingHelper(
                    inputs=decoder_inputs_embedded, 
                    sequence_length=self.decoder_targets_length,
                    embedding=embedding,
                    sampling_probability=sampling_prob,
                    time_major=False, name="training_helper")
                training_decoder = tf.contrib.seq2seq.BasicDecoder(
                    cell=decoder_cell, helper=training_helper,
                    initial_state=decoder_initial_state, output_layer=output_layer)

                decoder_outputs, _, _ = tf.contrib.seq2seq.dynamic_decode(
                    decoder=training_decoder, impute_finished=True,
                    maximum_iterations=self.max_target_sequence_length)

                self.decoder_logits_train = tf.identity(decoder_outputs.rnn_output)
                self.decoder_predict_train = tf.argmax(self.decoder_logits_train, axis=-1, name="decoder_pred_train")
                self.loss = tf.contrib.seq2seq.sequence_loss(logits=self.decoder_logits_train,
                                                             targets=self.decoder_targets, weights=self.mask)

                tf.summary.scalar("loss", self.loss)
                self.summary_op = tf.summary.merge_all()
                
                # Define optimizer
                optimizer = tf.train.AdamOptimizer(self.learning_rate)
                trainable_params = tf.trainable_variables()
                gradients = tf.gradients(self.loss, trainable_params)
                clip_gradients, _ = tf.clip_by_global_norm(gradients, self.max_gradient_norm)
                self.train_op = optimizer.apply_gradients(zip(clip_gradients, trainable_params))

            elif self.mode == "decode":
                start_tokens = tf.ones([self.batch_size, ], tf.int32) * self.word_to_idx["<go>"]
                end_token = self.word_to_idx["<eos>"]
                if self.beam_search:
                    inference_decoder = tf.contrib.seq2seq.BeamSearchDecoder(
                        cell=decoder_cell, 
                        embedding=embedding,
                        start_tokens=start_tokens, 
                        end_token=end_token,
                        initial_state=decoder_initial_state, 
                        beam_width=self.beam_size,
                        output_layer=output_layer)
                else:
                    decoding_helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(
                        embedding=embedding,
                        start_tokens=start_tokens, 
                        end_token=end_token)
                    inference_decoder = tf.contrib.seq2seq.BasicDecoder(
                        cell=decoder_cell, helper=decoding_helper,
                        initial_state=decoder_initial_state,
                        output_layer=output_layer)
                decoder_outputs, _, _ = tf.contrib.seq2seq.dynamic_decode(
                    decoder=inference_decoder,
                    maximum_iterations=50)
                if self.beam_search:
                    self.decoder_predict_decode = decoder_outputs.predicted_ids
                else:
                    self.decoder_predict_decode = tf.expand_dims(decoder_outputs.sample_id, -1)

        # Save model
        self.saver = tf.train.Saver(tf.global_variables())
    

    def train(self, batch):
        feed_dict = {self.encoder_inputs: batch.encoder_inputs,
                      self.encoder_inputs_length: batch.encoder_inputs_length,
                      self.decoder_targets: batch.decoder_targets,
                      self.decoder_targets_length: batch.decoder_targets_length,
                      self.keep_prob_placeholder: 0.5,
                      self.batch_size: len(batch.encoder_inputs)}
        _, loss, summary = self.sess.run([self.train_op, self.loss, self.summary_op], feed_dict=feed_dict)
        return loss, summary


    def eval(self, batch):
        feed_dict = {self.encoder_inputs: batch.encoder_inputs,
                      self.encoder_inputs_length: batch.encoder_inputs_length,
                      self.decoder_targets: batch.decoder_targets,
                      self.decoder_targets_length: batch.decoder_targets_length,
                      self.keep_prob_placeholder: 1.0,
                      self.batch_size: len(batch.encoder_inputs)}
        loss, summary = self.sess.run([self.loss, self.summary_op], feed_dict=feed_dict)
        return loss, summary


    def infer(self, batch):
        feed_dict = {self.encoder_inputs: batch.encoder_inputs,
                      self.encoder_inputs_length: batch.encoder_inputs_length,
                      self.keep_prob_placeholder: 1.0,
                      self.batch_size: len(batch.encoder_inputs)}
        predict = self.sess.run([self.decoder_predict_decode], feed_dict=feed_dict)
        return predict


    def infer_sent_emb(self, batch):
        feed_dict = {self.encoder_inputs: batch.encoder_inputs,
                      self.encoder_inputs_length: batch.encoder_inputs_length,
                      self.keep_prob_placeholder: 1.0,
                      self.batch_size: len(batch.encoder_inputs)}
        predict = self.sess.run([self.sent_emb], feed_dict=feed_dict)
        return predict
