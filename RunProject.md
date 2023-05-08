# Main
First run following command: chmod 777 run.sh

Next the main file can run. This will generate a couple of files:
* The dot-files in: compilers/src/ast/dotFiles
* The llvm output in: compilers/generated/output

These will be generated based on the input file compilers/input/input.c

# Tests
The test files can be uploaded into test_LLVM/input folder. And the expected llvm output
can be uploaded to test_LLVM/LLVM_expected