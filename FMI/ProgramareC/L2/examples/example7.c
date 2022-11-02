#include <stdio.h>

int main(){
	float n1, n2;
	printf("Enter 2 numbers: ");
	scanf("%f %f", &n1, &n2);
	if(n2 == 0)
		printf("Divizion by 0\n");
	else
		printf("%6.2f divided by %6.2f is: %6.2f\n", n1, n2, n1/n2);
	return 0;
}
