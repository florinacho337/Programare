#include <stdio.h>
#include <string.h>

int main(){
	char sir[100];
	gets(sir);
	int c = strlen(sir)-1;
	for (c; c >= 0; c--)
		printf("%c", *(sir + c));
	printf("\n");
	return 0;
}

