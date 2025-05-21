# Convert LLVM IR to object
llc out.ll -filetype=obj -o out.o

# Link into executable
clang out.o -o hello.exe
