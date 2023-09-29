#include <stdio.h>
void swap (int *a,int*b)
{
        int aux=*a;
        *a=*b;
        *b=aux;
}
int part(int s[],int st, int dr)
{
        int p=s[dr],i=st-1,j;
        for(j=st;j<dr;j++)
                if(s[j]<=p)
                        {
                                i++;
                                swap(&s[i],&s[j]);
                        }
        swap(&s[i+1],&s[dr]);
        return i+1;
}
void qS(int s[], int st, int dr)
{
        if(st<dr)
        {
                int p=part(s,st,dr);
                qS(s,st,p-1);
                qS(s,p+1,dr);
        }
}
int main()
{
        int s[]={5,2,4,1,9},n=5,i;
        printf("Initial array:\n");
        for(i=0;i<n;i++)
                printf("%d ",s[i]);
        qS(s,0,n-1);
        printf("Sorted array:\n");
        for(i=0;i<n;i++)
                printf("%d ",s[i]);
        return 0;
}
