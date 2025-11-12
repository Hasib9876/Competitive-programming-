#include<stdio.h>
int main()
{
    int a,b,c,d;
    double x,y,sum;
    scanf("%d %d %lf %d %d %lf",&a,&b,&x,&c,&d,&y);
    sum=(b*x)+(d*y);
    printf("VALOR A PAGAR: R$ %.2lf\n",sum);
    return 0;
}
