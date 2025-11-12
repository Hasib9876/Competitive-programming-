#include<stdio.h>
int main()
{
    double pai,r,sum;
    pai=3.14159;
    scanf("%lf",&r);
    sum=(4*pai*r*r*r)/3;
    printf("VOLUME = %.3lf\n",sum);
    return 0;
}
