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
    ;(a-b+c*128)/(a+b)+e-x    a,b - byte  c - word   e - dword  x - qword
    a db 15
    b db -10
    c dw 3
    e dd 11
    x dq  -5
    r dq 0
; our code starts here
segment code use32 class=code
    start:
        ; ...(a-b+c*128)/(a+b)+e-x fara semn
        ;rezultat: 2E
        ;c*128 in dx:ax
        mov ax, 128
        mul word[c]
        ;a + c * 128 in dx:ax
        add al, [a]
        adc dx, 0
        ;a-b+c*128 in dx:ax
        mov bx, 0
        mov bl, [b]
        sub ax, bx
        sbb dx, 0
        ;a+b in bx
        mov bx, 0
        mov bl, [a]
        add bl, [b]
        ;(a-b+c*128)/(a+b) = ax rest dx
        div bx
        ;convert ax to eax
        push ax
        mov eax, 0
        pop ax
        ;(a-b+c*128)/(a+b)+e in eax
        add eax, [e]
        ;(a-b+c*128)/(a+b)+e-x in edx:eax
        mov edx, 0
        sub eax, dword[x]
        sbb edx, dword[x+4]
        ;salvam rezultatul in r
        mov dword[r],  eax
        mov dword[r+4], edx
        ;(a-b+c*128)/(a+b)+e-x cu semn
        ; rezultat FFFFFFC9
        ;c*128 in dx:ax apoi in stiva
        mov al, 128
        cbw
        imul word[c]
        push dx
        push ax
        ;a + c*128 in ebx
        movsx eax, byte[a]
        pop ebx
        add ebx, eax
        ;a-b+c*128 in ebx apoi mutam rezultatul in dx:ax
        movsx eax, byte[b]
        sub ebx, eax
        push ebx
        pop ax
        pop dx
        ;a+b in cx
        movsx  cx, byte[a]
        movsx bx, byte[b]
        add cx, bx
        ;(a-b+c*128)/(a+b) = ax rest dx
        idiv cx
        ;(a-b+c*128)/(a+b)+e in eax
        cwde
        add eax, [e]
        cdq
        ;(a-b+c*128)/(a+b)+e-x in edx:eax
        sub eax, dword[x]
        sbb edx, dword[x+4]
        ;(a-b+c*128)/(a+b)+e-x fara semn in ecx:ebx si 000000000000002E
        ;(a-b+c*128)/(a+b)+e-x cu semn in edx:eax FFFFFFFFFFFFFFC9
        mov ebx, dword[r]
        mov ecx, dword[r+4]
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
