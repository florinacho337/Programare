bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data
    ; ...
    a db 11100110b
    b dw 0f1a3h 
    c dd 067dafh
    r dw 0

; our code starts here
segment code use32 class=code
    start:
        ; ...
        or word[r], 00000000000011111b
        mov bx, [b]
        not bx
        shr bx,  8 ; bx = 00000000 b(15-8)
        and bx, 0000000011100000b ; bx = 00000000 b(15-13) 00000
        or word[r], bx
        mov al, [a]
        cbw; ax = a(15-0) 
        shl ax, 8; ax = a(7-0)00000000b
        and ax, 0001111100000000b; ax = 000 a(4-0) 00000000b
        or word[r], ax
        mov ebx, [c]
        shr ebx, 7; ebx = 0000000 c(31-7)
        and bx, 1110000000000000b ; bx = c(22-20) 0000000000000b
        or word[r], bx
        
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
