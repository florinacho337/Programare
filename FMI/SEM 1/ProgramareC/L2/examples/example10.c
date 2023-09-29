#include <stdio.h>

int main(){
	char ch[101] = "Acesta este un string";
	int vowels = 0, nonvowels = 0;
	int i = 0;
	while(ch[i]){
		switch(ch[i]){//counts lowercase vowels and nonvowels
			case 'a':
			case 'e':
			case 'i':
			case 'o':
			case 'u': vowels++;
				  break;
			default: nonvowels++;
				 break; //not needed, just for clarity
		}
		i++;
	}
	puts(ch);
	printf("Vowels: %d\nNonvowels: %d\n", vowels, nonvowels);
	return 0;
}
		      
