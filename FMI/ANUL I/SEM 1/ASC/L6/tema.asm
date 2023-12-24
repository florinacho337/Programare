bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data
    ; Se da un sir de cuvinte s. Sa se construiasca sirul de octeti d, astfel incat d sa contina pentru fiecare pozitie din s:
    ; - numarul de biti de 0, daca numarul este negativ
    ; - numarul de biti de 1, daca numarul este pozitiv
    ; d : 3, 3, 5, 7
    s dw -22 , 145, -48, 127
    ls equ ($-s)/2
    d resb ls
    copie db 0

; our code starts here
segment code use32 class=code
    start:
        ; ...
         mov esi, s
         mov edi, d
         mov ecx, ls
         mov eax, 0
         cld
         repeta1:
            lodsw ; AX <-- [esi]
            mov [copie], ecx
            mov ecx, 15
            mov edx, 0
            repeta2:
                mov ebx, 1
                and ebx, eax
                add edx, ebx
                shr ax, 1
            loop repeta2
            mov ecx, [copie]
            cmp al, 1
            je negativ
            jne pozitiv
            negativ:
                add edx, 1
                mov al, 16
                sub eax, edx
                stosb ; [edi] <-- al
                loop repeta1
            pozitiv:
                mov eax, edx
                stosb ; [edi] <-- al
                loop repeta1
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
