# Main
First run following command: chmod 777 run.sh

Next the main file can run. This will generate a couple of files:
* The dot-files in: compilers/src/ast/dotFiles
* The llvm output in: compilers/generated/output

These will be generated based on the input file compilers/input/input.c

# Tests
The file compilers/src/TestCases/CToLLVM_Tests.py can be run separately to check the behavior of the parser.
These tests will run all files from compilers/src/TestCases/InputFiles. 

For the file that is supposed to compile nicely (compilers/src/TestCases/InputFiles/fullExample.c) the generated
llvm file is compared with the expected output from compilers/src/TestCases/ExpectedResults/llvm_fullExample.ll.

Next the files that should generate errors are run and the generated error is compared with the expected error for
the corresponding input file.

For all tests that get to the point of generating the AST the corresponding dot-files are generated and placed in 
compilers/src/TestCases/DotFiles.