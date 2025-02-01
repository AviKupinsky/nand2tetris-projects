@256
D=A
@SP
M=D
@function_return0
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
 @0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JEQ

(function_return0)

//C_FUNCTION function Main.fibonacci 0 
(Main.fibonacci)


//C_PUSH push argument 0 
@ARG
D=M
@0
D=D+A
@13
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH push constant 2 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_ARITHMETIC lt 
@SP
AM=M-1
D=M
@R13
M=D
@part6lt0
D;JGE
@SP
AM=M-1
D=M
@part5lt0
D;JGE
@R13
D=D-M
@part4lt0
D;JGE
D=-1
@lt0end
0;JMP
(part4lt0)
D=0
@lt0end
0;JMP
(part5lt0)
D=0
@lt0end
0;JMP
(part6lt0)
@SP
AM=M-1
D=M
@part7lt0
D;JGE
D=-1
@lt0end
0;JMP
(part7lt0)
@R13
D=D-M
@part8lt0
D;JGE
D=-1
@lt0end
0;JMP
(part8lt0)
D=0
@lt0end
0;JMP
(lt0end)
@SP
AM=M+1
A=A-1
M=D

//C_IF if-goto IF_TRUE 
@SP
AM=M-1
D=M
@IF_TRUE
D;JNE

//C_GOTO goto IF_FALSE 
@IF_FALSE
0;JEQ

//C_LABEL label IF_TRUE 
(IF_TRUE)

//C_PUSH push argument 0 
@ARG
D=M
@0
D=D+A
@13
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_RETURN 
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
 AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M-1
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@14
A=D
0;JEQ

//C_LABEL label IF_FALSE 
(IF_FALSE)

//C_PUSH push argument 0 
@ARG
D=M
@0
D=D+A
@13
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH push constant 2 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_ARITHMETIC sub 
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

//C_CALL call Main.fibonacci 1 
@function_return1
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
 @1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JEQ

(function_return1)

//C_PUSH push argument 0 
@ARG
D=M
@0
D=D+A
@13
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH push constant 1 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_ARITHMETIC sub 
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

//C_CALL call Main.fibonacci 1 
@function_return2
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
 @1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JEQ

(function_return2)

//C_ARITHMETIC add 
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D

//C_RETURN 
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
 AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M-1
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@14
A=D
0;JEQ

//C_FUNCTION function Sys.init 0 
(Sys.init)


//C_PUSH push constant 4 
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_CALL call Main.fibonacci 1 
@function_return3
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
 @1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JEQ

(function_return3)

//C_LABEL label WHILE 
(WHILE)

//C_GOTO goto WHILE 
@WHILE
0;JEQ

