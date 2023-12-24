#include <stdio.h>

int main(){
	printf("Fill zeros\n---\n");
	printf("%03d\n",0);
	printf("%03d\n",-1);
	printf("%03d\n",12345);
	printf("%03d\n",-12345);
	printf("Invisible + Sign\n---\n");
	printf("% -3d\n",0);
	printf("% -3d\n",-1);
	printf("% -3d\n",12345);
	printf("% -3d\n",-12345);
	return 0;
}
