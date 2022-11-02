#include <stdio.h>

int main(){
	int n, nfact = 1;
	printf("Enter a number >0: ");
	scanf("%d", &n);
	while(n > 0){
		nfact *= n;
		n -= 1;
	}
	printf("Value of factorial is: %d \n", nfact);
	return 0;
}
