#include <stdio.h>
#include <limits.h>
#include <float.h>
int main(void){
	printf("An int occupies: %ld bytes \n", sizeof(int));
	printf("Smallest int is: %d\n", INT_MIN);
	printf("Greatest int is: %d\n\n", INT_MAX);
	printf("A double occupies: %ld bytes \n", sizeof(double));
	printf("Smallest double is: %e\n", DBL_MIN);
	printf("Greatest double is: %e\n", DBL_MAX);
	return 0;
}

