#include <stdio.h>
#include <limits.h>

int main(){
	int maxim = INT_MIN, minim = INT_MAX, n;
	printf("Enter five values:\n");
	for(int i = 1; i <= 5; ++i){
		scanf("%d", &n);
		if(n > maxim)
			maxim = n;
		if(n < minim)
			minim = n;
	}
	printf("The largest value is: %d, and the smallest is: %d\n", maxim, minim);
	return 0;
}
