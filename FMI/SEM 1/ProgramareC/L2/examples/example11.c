/* C program to print the average of n numbers and each 
 difference to the average. */
#include <stdio.h>

int main(){
	int number[100];
	float sum, average;
	int n = 0; //we guard against undef value n
	do{
		printf("Give the value for n (1-100)");
		scanf("%d", &n);
	} while(n < 1 || n > 100);
	sum = 0;
	for(int i = 0; i < n; i++){
		scanf("%d", &number[i]);
		sum += number[i];
	}
	average = sum/n;
	printf("\nAverage of the %d numbers is %7.2f\n", n, average);
	/* In order to print the difference between each
	 element and the average, we need to iterate
	 through the array */
	for(int i = 0; i < n; i++)
		printf("For the element %d, the difference between %d and average %7.2f is: %7.2f\n", i, number[i], average, number[i]-average);
	return 0;
}
