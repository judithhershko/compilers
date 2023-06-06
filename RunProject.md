# START PROJECT
In run.sh the antlr will generate the files for the grammar.
use the following command:

    chmod 777 run.sh
    ./run.sh
# MAIN
To test an input file use input/input.c . In this file you can put the c-code you want to test.
This will generate the following:

- mips code in generated/output.mars_output.asm
- dot file in src/ast/dotFiles/no_folded_expression_dot.dot

To visualise this use command:

    dot -Tpng src/ast/dotFiles/no_fold_expression_dot.dot -o generated/output/result.png

# TESTS

To run mips tests go to testMips/Mips_Tests.py. 
This file contains all the tests (passes and error checking) for this part of the project. 
