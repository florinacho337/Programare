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
    a db 245
    b db 192
    c db 212
    d dw 19764
    c1 db 10
    c2 db 2
    d2 db 155
    e dw 10765
    f dw 25897
    g dw 41765
    h dw 9576
    rez1 dw 0
    rez2 dd 0

; our code starts here
segment code use32 class=code
    start:
        ; ...
        ;I.[(10+d)-(a*a-2*b)]/c
        ;1.10+d
        movzx bx, byte[c1] 
        add bx, [d]
        ;2. 2*b in cx
        mov al, [c2]
        mul byte[b]
        mov cx, ax
        ;3. a*a
        movzx ax, byte[a]
        mul byte[a]
        ;4. a*a-2*b
        sub ax, cx
        ;5. (10+d)-(a*a-2*b)
        sub bx, ax
        mov ax, bx
        ;6.(10+d)-(a*a-2*b)/c
        div byte[c]
        mov byte[rez1+1], al
        mov byte[rez1+0], ah
        
        
        ;II.(f*g-a*b*e)/(h+c*d2)
        ;1.h + c * d2
        mov ax, [c]
        mul byte[d2]
        add ax, [h]
        mov bx, ax
        ;2. a*b*e in ecx
        mov ax, [a]
        mul byte[b]
        mul word[e]
        mov word[rez2+0],  ax
        mov word[rez2+2], dx
        mov ecx, [rez2]
        ;3.f*g
        mov ax, [f]
        mul word[g]
        mov word[rez2+0], ax
        mov word[rez2+2], dx
        ;4.f*g-a*b*e
        sub [rez2], ecx
        ;5.(f*g-a*b*e)/(h+c*d2)
        mov dx, word[rez2+2]
        mov ax, word[rez2+0]
        div bx
        mov word[rez2+0], dx
        mov word[rez2+2], ax
        mov ebx, [rez2]
        movzx eax, word[rez1]
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
