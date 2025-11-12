#include<stdio.h>
int main()
{
    double a,b,sum;
    char c[10];
    scanf("%s %lf %lf",&c,&a,&b);
    sum=a+(b*.15);
    printf("TOTAL = R$ %.2lf\n",sum);
    return 0;
}
