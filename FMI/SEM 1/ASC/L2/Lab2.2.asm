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
    a dw 2
    c db 15
    b dd 4
    x dd 10
    y dq 1
    aux dd 1; rezerva 1 doubleword pentru aux
                       ; echiv cu aux dd 0
; our code starts here
segment code use32 class=code
    start:
        ; ...
    mov ax, 3
        mul word[a]; dx:ax = a * 3
        ; salvare dx:ax
        mov word[aux+0], ax
        mov word[aux+2], dx
        
        ;c/b
        ;byte/doubleword
        ;byte -> edx:eax
        
        movzx eax, byte[c]
        mov edx, 0
        div dword[b]
        ;eax = catul c/b
        ;a*3 - c/b
        ;aux - eax
        ;doubleword - doubleword
        sub [aux], eax ; aux - a*3 - c/b
        ;a*3 - c/b + x
        ;          aux + x
        ;            dd + dd
        
        mov ebx, [aux]
        add ebx, [x]
        ; ebx = a*3 - c/b + x
        
        ;a*3 - c/b + x - y
        ;                  ebx - y
        ;                   dd - dq
        ;                   32 - 64
        ; transform ebx la 64 biti
        ;adica ebx -> ecx:ebx
        mov ecx, 0
        
        ;transfera y in edx:eax
        mov eax, dword[y+0]
        mov edx, dword[y+4]
        
        sub ebx, eax
        sbb ecx, edx
        ;ecx:edx
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
