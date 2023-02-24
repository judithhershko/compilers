#!/bin/bash

# start folder=compilers
export PYTHONPATH=$PYTHONPATH:src


#generate visitor and listener file
java -jar antlr-4.12.0-complete.jar -Dlanguage=Python3 Expressions.g4 -visitor;
#execute main
python3 main.py Expressions.g4
#install bindings for AST
#pip install antlr4-python3-runtime