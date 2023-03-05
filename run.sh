#!/bin/bash

# start folder=compilers
export PYTHONPATH=$PYTHONPATH:src

if [[ ! -f "antlr-4.12.0-complete.jar" ]]; then
  wget https://www.antlr.org/download/antlr-4.12.0-complete.jar
fi
#generate visitor and listener file
java -jar antlr-4.12.0-complete.jar -o generated -visitor -listener -Dlanguage=Python3 input/Expression.g4;
#execute main
#python3 main.py input/Expression.g4
python3 main.py input/input.c

dot -Tpng dotFiles/*.dot -o dotFiles/result.png

#install bindings for AST
#pip install antlr4-python3-runtime