bits 32
global main

extern scanf

extern printf

extern exit

section .data
	a times 4 db 0
	b times 4 db 0
	format db "%d", 0

section .text
	main:
		push a
		push format
		call scanf
		add ESP, 4 * 2

		mov BL, 5
		mov AL, 7
		mul byte [a]
		add BL, AL
		mov AL, 2
		mov DL, 4
		mul DL
		sub BL, AL
		mov [b], BL

		push dword [b]
		push format
		call printf
		add ESP, 4 * 2

		push 0
		call exit
