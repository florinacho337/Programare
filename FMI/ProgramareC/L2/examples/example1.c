#include <stdio.h>

int main(){
	int var1 = 5, var2 = 10, var3 = 12;
	printf("hello world\n");
	printf("%s\n", "hello world");
	printf("%d, %d\t%d\n", var1, var2, var3); // \t = Tab, \n = New Line
	printf("%f, \b%f\n", (double)var1, (double)var2); // \b = Backspace
	return 0;
}
