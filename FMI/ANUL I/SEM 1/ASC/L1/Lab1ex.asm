bits 32

global start        

extern exit 
import exit msvcrt.dll

segment data use32 class=data
    a db 1Ah
    b dw 00BCh
    c dd Ch

segment code use32 class=code
    start:
        mov AL, [a]
        mov BX, [b]
        mov ECX, [c]
        push    dword 0
        call    [exit]
