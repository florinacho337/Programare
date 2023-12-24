bits 32

global start        

extern exit 
import exit msvcrt.dll

segment data use32 class=data
    x dd 2
    y db 3

segment code use32 class=code
    start:
        mov eax, 010b
        sub eax, [x]
        ;[ ] pentru a accesa valoarea unei variabile
        
        ;y de la byte sa fie extins la doubleword
        movzx ebx, byte[y]
        sub eax, ebx
        ; eax =0101b - x - y
        
        push    dword 0
        call    [exit]
