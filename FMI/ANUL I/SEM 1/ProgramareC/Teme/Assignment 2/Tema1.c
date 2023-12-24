#include <stdio.h>

int main(){
	unsigned int a[100], n;
	printf("Enter how many values do you want to show from Fibonacci Series (<=100):\n");
	scanf("%u", &n);
	a[0] = a[1] = 1;
	for(int i = 2; i < n; ++i)
		a[i] = a[i-2] + a[i-1];	
	for(int i = 0; i < n; ++i)
		printf("%u ", a[i]);
	printf("\n");
	return 0;
}
