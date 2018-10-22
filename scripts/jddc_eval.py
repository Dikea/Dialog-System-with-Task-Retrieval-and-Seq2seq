#!/usr/bin/python3


import sys
sys.path.append("smart_dialog_system")
from run_model import run_prediction

input_file = sys.argv[1]
output_file = sys.argv[2]

run_prediction(input_file, output_file)
