#include <stdio.h>
#include <stdlib.h>

int main(){
	//memory allocation
	int** mat1 = (int**)malloc(5*sizeof(int*));
	for(int i = 0; i < 5; ++i)
		mat1[i] = (int*)malloc(4*sizeof(int));
	int** mat2 = (int**)malloc(4*sizeof(int*));
	for(int i = 0; i < 4; ++i)
		mat2[i] = (int*)malloc(5*sizeof(int));
	int** mat3 = (int**)malloc(5*sizeof(int*));
	for(int i = 0; i < 5; ++i)
		mat3[i] = (int*)malloc(5*sizeof(int));
	//value assignment
	printf("Enter values for a 5x4 matrix:\n");
	for(int i = 0; i < 5; ++i)
		for(int j = 0; j < 4; ++j)
			scanf("%d", &mat1[i][j]);
	printf("Enter values for a 4x5 matrix:\n");
	for(int i = 0; i < 4; ++i)
		for(int j = 0; j < 5; ++j)
			scanf("%d", &mat2[i][j]);
	//multiply operation
	for(int i = 0; i < 5; i++)
		for(int j = 0; j < 5; j++){
			int rez = 0;
			for(int k = 0; k < 4; k++)
				rez = rez + mat1[i][k]*mat2[k][j];
			mat3[i][j] = rez;
		}
	//print result
	printf("The result of multiplication is:\n");
	for(int i = 0; i < 5; i++){
		for(int j = 0; j < 5; j++)
			printf("%d ", mat3[i][j]);
		printf("\n");
	}
	//deallocate memory
	for(int i = 0; i < 5; ++i)
		free(mat1[i]);
	free(mat1);
	for(int i = 0; i < 4; ++i)
		free(mat2[i]);
	free(mat2);
	for(int i = 0; i < 5; ++i)
		free(mat3[i]);
	free(mat3);
	return 0;
}


	
