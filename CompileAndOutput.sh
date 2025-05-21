python compile.py math_control.vc
llc out.ll -filetype=obj -o out.o
clang out.o -o math.exe
./math.exe
