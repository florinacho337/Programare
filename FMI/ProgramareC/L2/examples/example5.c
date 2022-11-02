#include <stdio.h>

int main(){
	float nr=1.8765432;
	printf(" Precision digits\n");
	printf("%.0f\n",nr);
    	printf("%.0f.\n",nr);
	printf("%.1f\n",nr);
	printf("%.6f\n",nr);
	printf("Width and precision\n-----\n");
	printf("%5.0f\n",nr);
	printf("%5.0f.\n",nr);
	printf("%5.1f\n",nr);
	printf("%5.6f\n",nr);
	return 0;
}
