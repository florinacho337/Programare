#include <stdio.h>

int main(){
	printf("Fill spaces\n---\n");
	printf("%-3d\n", 0);
	printf("%-3d\n",-1);
	printf("%-3d\n",12345);
	printf("%-3d\n",-12345);
	printf("Justify\n---\n");
	printf("%+3d\n",0);
	printf("%+3d\n",-1);
	printf("%+3d\n",12345);
	printf("%+3d\n",-12345);
	return 0;
}
