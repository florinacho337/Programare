#include <stdio.h>

void fibonacci(int n){
	int f1 = 1, f2 = 1;
	if(n == 1)
		printf("%d", f1);
	else{
		printf("%d %d", f1, f2);
		for(int i = 3; i <= n; ++i){
			int f3 = f1 + f2;
			f1 = f2;
			f2 = f3;
			printf(" %d", f3);
		}
	}
}

int main(){
	int k;
	printf("Enter how many numbers do you want to show from Fibonacci Series:\n");
	scanf("%d", &k);
	fibonacci(k);
	printf("\n");
	return 0;
}
