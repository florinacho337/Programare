#include <stdio.h>
#include <limits.h>
#define SIZE 10

int main(){
	int matrix[SIZE][SIZE], maxim = INT_MIN;
	printf("Enter the numbers:\n");
	for(int i = 0; i < SIZE; ++i)
		for(int j = 0; j < SIZE; ++j){
			scanf("%d", &matrix[i][j]);
			if(matrix[i][j] > maxim)
				maxim = matrix[i][j];
		}
	printf("The largest value is %d.\n", maxim);
	return 0;
}
