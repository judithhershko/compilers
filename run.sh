#!/bin/bash

# start folder=compilers
export PYTHONPATH=$PYTHONPATH:src

if [[ ! -f "antlr-4.12.0-complete.jar" ]]; then
  wget https://www.antlr.org/download/antlr-4.12.0-complete.jar
fi

#generate visitor and listener file
java -jar antlr-4.12.0-complete.jar -o generated -visitor -listener -Dlanguage=Python3 input/Expression.g4;

#main file
python3 main.py
#tests
python3 src/TestCases/CToLLVM_Tests.py

dot -Tpng generated/output/result.dot -o generated/output/result.png