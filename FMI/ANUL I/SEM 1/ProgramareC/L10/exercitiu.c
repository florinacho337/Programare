#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	FILE *fp;
	int c, i = 1;
	char buff[1000];
	fp = fopen("file1.txt", "r");
	while(1){
		if(fgets(buff, 1000, fp) == NULL) break;
		if(i % 2 == 1)
			for(c = (int)strlen(buff); c >= 0; c--)
				printf("%c", buff[c]);
		else
			for(c = 0; c <= (int)strlen(buff); c++)
				printf("%c", buff[c]);
		printf("\n");
		i++;
	}
	return 0;
}
