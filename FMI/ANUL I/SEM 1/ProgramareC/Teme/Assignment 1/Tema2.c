#include <stdio.h>
/*
Given as input a floating number of centimeters, print the corresponding number offeet (integer) and inches (floating, 1 decimal), with the inches given to anaccuracy of one decimal place.Assume 2.54 centimeters per inch, and 12 inches per foot. 
*/
int main(){
	float centimeters;
	printf("Enter a number of centimeters to convert in feet: ");
	scanf("%f", &centimeters);
	float inches = centimeters / 2.54;
	float feet = inches / 12;
	inches = inches - (int)feet*12;
	printf("The result is: %d feet and %1.1f inches.\n", (int)feet, inches);
	return 0;
}
