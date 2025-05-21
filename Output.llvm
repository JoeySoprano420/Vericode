@fmt_1 = internal constant [4 x i8] c"%d\0A\00"
@fmt_2 = internal constant [4 x i8] c"%f\0A\00"

define void @main() {
entry:
  %age = alloca i32
  store i32 42, i32* %age
  %pi = alloca double
  store double 0x40091EB851EB851F, double* %pi
  %0 = load i32, i32* %age
  call i32 (i8*, ...) @printf(i8* bitcast ([4 x i8]* @fmt_1 to i8*), i32 %0)
  %1 = load double, double* %pi
  call i32 (i8*, ...) @printf(i8* bitcast ([4 x i8]* @fmt_2 to i8*), double %1)
  ret void
}
