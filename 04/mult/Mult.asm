// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

@R2
M=0

@i
M=0

@R0
D=M

@FIRST
M=D

@R1
D=M

@SECOND
M=D



(NEW1)
    @FIRST
    M=-M
    @SECOND
    M=-M

(LOOP)
    // if(i==R1)goto END
    @FIRST
    D=M
    @NEW1
    D;JLT
    @i
    D=D-M
    @END
    D;JEQ

    //RAM[R2]=RAM[R2] + RAM[R0]
    @SECOND
    D=M
    @R2
    M=M+D
    @i
    M=M+1
    @LOOP
    0;JMP





(END)
    @END
    0;JMP


   
   