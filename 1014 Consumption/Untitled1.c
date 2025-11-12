#include<stdio.h>
int main()
{
    int X;
    double Y,sum;
    scanf("%d %lf",&X,&Y);
    sum=X/Y;
    printf("%.3lf km/l\n",sum);
    return 0;
}
