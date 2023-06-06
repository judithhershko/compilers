#!/bin/bash

# start folder=compilers
export PYTHONPATH=$PYTHONPATH:src

if [[ ! -f "antlr-4.12.0-complete.jar" ]]; then
  wget https://www.antlr.org/download/antlr-4.12.0-complete.jar
fi

#generate visitor and listener file
java -jar antlr-4.12.0-complete.jar -o generated -visitor -listener -Dlanguage=Python3 input/Expression.g4;

dot -Tpng src/ast/dotFiles/no_fold_expression_dot.dot -o generated/output/result.png