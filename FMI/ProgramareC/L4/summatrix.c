#include <stdio.h>
int main()
{
        int n, m, i,j,a[101][101];
  printf("Introduceti numarul de linii al matricei:\n");
  scanf("%d", &n);
  printf("Introduceti numarul de coloane al matricei:\n");
  scanf("%d", &m);
  for(i=1; i<=n; i++)
  {
        printf("Introduceti elementele din linia %d a matricei:\n", i);
        for(j=1; j<=m; j++)
        scanf("%d", &a[i][j]);
        }
  int sum;
  for(i=1; i<=n; i++)
  {
    sum = 0;
    for(j=1; j<=m; j++)
        sum += a[i][j];
    printf("Suma elementelor de pe linia %d a matrice este:%d\n", i, sum);
  }
  return 0;
}

  
