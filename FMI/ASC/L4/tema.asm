bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data
    ; Se da octetul A. Sa se obtina numarul intreg n reprezentat de bitii 2-4 ai lui A. 
    ; Sa se obtina apoi in B octetul rezultat prin rotirea spre dreapta a lui A cu n pozitii. Sa se obtina dublucuvantul C:
    ; bitii 8-15 ai lui C sunt 0
    ; bitii 16-23 ai lui C coincid cu bitii lui B
    ; bitii 24-31 ai lui C coincid cu bitii lui A
    ; bitii 0-7 ai lui C sunt 1
    a db 65h
    n db 0
    b db 0
    c dd 0
; our code starts here
segment code use32 class=code
    start:
        ; ...
        ;1. aflam numarul intreg n
        mov al, [a] ; 01100101 - 65h
        and al, 00011100b; 00000100 - 04h
        shr al, 2; 00000001 - 01h
        mov [n], al; n = 01h = 1
        ;2. obtinem octetul b
        mov al, [a]; 01100101 - 65h
        mov cl, [n]
        ror al, cl; 10110010 - B2h
        mov [b], al; b = B2h
        ;3. obtinem dword-ul c
        mov al, [a]
        mov bl, [b]
        or byte[c+1], bl
        or byte[c+3], 11111111b
        or byte[c], al
        ;c = 01100101101100100000000011111111 = 65B200FFh
        mov ecx, [c]
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
