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
    a db 50
    b dw 1000
    c dw 5000
    d dd 90192
    
    ; our code starts here
segment code use32 class=code
    start:
        ; ... (a*b) + (c*d) fara semn
        ; a*b in  ebx
        mov ax, 0
        mov al, [a]
        mul word[b]
        push dx
        push ax
        pop ebx
        ;c*d in edx:eax
        mov eax, 0
        mov ax, c
        mul dword[d]
        ;(a*b) + (c*d) in edx:eax
        add eax, ebx
        ; (a*b) + (c*d) cu semn
        ; a*b in ebx
        mov al, [a]
        cbw
        imul word[b]
        push dx
        push ax
        pop ebx
        ;c*d in edx:eax
        mov ax, [c]
        cwde
        imul dword[d]
        ;(a*b) + (c*d) in edx:eax
        add eax, ebx
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
