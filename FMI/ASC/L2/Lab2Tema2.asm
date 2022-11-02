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
    a db 70
    b db 12
    c db 22
    d db 41
    a1 dw 7564
    b1 dw 4219
    c1 dw 3590
    d1 dw 21015

; our code starts here
segment code use32 class=code
    start:
        ; ...
        ;(a-b-b-c)+(a-c-c-d)
        mov eax, 0
        mov al, [a]
        sub al, [b]
        sub al, [b]
        sub al, [c]
        mov edx, 0
        mov dl, [a]
        sub dl, [c]
        sub dl, [c]
        sub dl, [d]
        sub al, dl
        ;a1+b1-(c1+d1)+100h
        mov eax, 0
        mov ax, [a1]
        add ax, [b1]
        mov edx, 0
        mov dx, [c1]
        add dx, [d1]
        sub ax, dx
        add ax, 100h
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
