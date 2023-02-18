#!/bin/bash

# start folder=compilers
export PYTHONPATH=$PYTHONPATH:src

# Downloads the jar if it does not exists
if [[ ! -f "antlr-4.8-complete.jar" ]]; then
  wget https://www.antlr.org/download/antlr-4.8-complete.jar
fi;
#generate visitor and listener file
antlr4 -Dlanguage=Python3 Expr.g4 -visitor;
#execute main
python3 main.py Expr.g4