#include<stdio.h>
int main()
{
	int *p,*q;
	int s,a,b;
	printf("Enter 2 numbers:");
	scanf("%d %d",&a,&b);
      	p=&a;
      	q=&b;
      	s=*p+*q;
      	printf("%d+%d=%d",*p,*q,s);
      	return 0;
}
