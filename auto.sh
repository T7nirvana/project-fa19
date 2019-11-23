#!/bin/bash
python3 ./algs/input_generator.py $1
python3 solver.py --all inputs outputs
python3 input_validator.py --all inputs
python3 output_validator.py --all inputs outputs
