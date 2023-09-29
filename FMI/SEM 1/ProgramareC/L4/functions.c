#include <stdio.h>

float reciprocal(int n){
	float nr = (float)n;
	return 1/nr;
}

float square(int n){
	return (float)n*n;
}

void performtask(int n1, int n2, float (*function)(int)){
	for(int i = n1; i <= n2; ++i)
		printf("%.5f\n", function(i));
}

int main(){
	int k = 5;
	performtask(1, k, square);
	printf("-----------------\n");
	performtask(1, k, reciprocal);
	return 0;
}
