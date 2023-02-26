#!/bin/bash

# start folder=compilers
export PYTHONPATH=$PYTHONPATH:src


#generate visitor and listener file
java -jar antlr-4.12.0-complete.jar -o generated -visitor -listener -Dlanguage=Python3 input/Expression.g4;
#execute main
python3 main.py input/Expression.g4
#install bindings for AST
#pip install antlr4-python3-runtime