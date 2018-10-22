#!/bin/env python
#-*- encoding: utf-8 -*-


import tensorflow as tf


def create_rnn_cell(unit_type, num_units, num_layers, 
                    dropout, mode, forget_bias = 1.0):
    """Create multi-layer RNN cell."""
    cell_list = []
    for i in range(num_layers):
        single_cell = _single_cell(
            unit_type = unit_type,
            num_units = num_units,
            forget_bias = forget_bias,
            dropout = dropout,
            mode = mode)
        cell_list.append(single_cell)
    if len(cell_list) == 1:
        return cell_list[0]
    else: 
        return tf.contrib.rnn.MultiRNNCell(cell_list)


def _single_cell(unit_type, num_units, dropout, mode, forget_bias = 1.0):
    """Create an instance of a single RNN cell.""" 
    # Dropout (equal 1 - keep_prob) is set to 0 during eval and infer
    dropout = dropout if mode == tf.contrib.learn.ModeKeys.TRAIN else 0.0

    if unit_type == 'lstm':
        single_cell = tf.contrib.rnn.BasicLSTMCell(
            num_units,
            forget_bias = forget_bias)

    if dropout > 0.0:
        single_cell = tf.contrib.rnn.DropoutWrapper(
            cell = single_cell, 
            input_keep_prob = (1.0 - dropout))

    return single_cell


def save_model(save_path, sess, inputs, outputs):
    """Save model"""
    if tf.gfile.Exists(save_path):
        tf.gfile.DeleteRecursively(save_path)
    builder = tf.saved_model.builder.SavedModelBuilder(save_path)
    inputs_ = {k: tf.saved_model.utils.build_tensor_info(v)
        for k, v in inputs.iteritems()}
    outputs_ = {k: tf.saved_model.utils.build_tensor_info(v)
        for k, v in outputs.iteritems()}
    signature = tf.saved_model.signature_def_utils.build_signature_def(
        inputs_, outputs_, 'signature_')
    builder.add_meta_graph_and_variables(sess, ['saved_model'], 
        signature_def_map = {'signature': signature})
    builder.save()


def get_model_tensor(save_path, sess, inputs_fields, outpus_fields):
    """Load model"""
    meta_graph_def = tf.saved_model.loader.load(sess, 
        ['saved_model'], save_path)
    signature = meta_graph_def.signature_def
