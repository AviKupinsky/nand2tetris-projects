// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(MAIN)
    @SCREEN
    D=A
    @IDENTITY
    M=D

    @I
    M=0


    @KBD
    D=M
    
    @BLACK
    D;JGT

    @COLOR
    M=0 
    @LOOP
    0;JMP

(BLACK)
     @COLOR
     M=-1


(LOOP)
    @8192
    D=A
    @I
    D=D-M
    @MAIN
    D;JEQ


    @COLOR
    D=M
    @IDENTITY
    A=M
    M=D
    
    @I
    M=M+1
    @IDENTITY
    M=M+1
    @LOOP
    0;JMP