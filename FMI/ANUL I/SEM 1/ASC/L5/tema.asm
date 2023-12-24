bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data
    ; Se dau doua siruri de caractere S1 si S2. Sa se construiasca sirul D prin concatenarea 
    ; elementelor de pe pozitiile multiplu de 3 din sirul S1 cu elementele sirului S2 in ordine inversa.
    s1 db '+', '4', '2', 'a', '8', '4', 'X', '5'
    ls1 equ $-s1
    s2 db 'a', '4', '5'
    ls2 equ $-s2
    d resb (ls1+2) / 3 + ls2

; our code starts here
segment code use32 class=code
    start:
        ; ...
        mov esi, s1 ; adresa lui s1
        mov ecx, 1
        mov edi, d ; adresa lui d
        repeta1:
            mov al, [esi]
            mov [edi], al; se adauga elementul de la adresa esi in sirul d pe pozitia de la adresa edi
            add esi, 3 
            inc edi 
            add ecx, 3
            cmp ecx, ls1
        jbe repeta1
         
        mov esi, s2 + ls2 - 1
        mov ecx, ls2
        repeta2:
            mov al, [esi]
            mov [edi], al ; se adauga elementul de la adresa esi in sirul d pe pozitia de la adresa edi
            inc edi
            dec esi
        loop repeta2
        ;D: '+', 'a', 'X', '5', '4', 'a'
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
