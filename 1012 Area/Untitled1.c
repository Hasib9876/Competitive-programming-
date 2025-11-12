#include<stdio.h>
int main()
{
    double a,b,c,pai=3.14159,sum1,sum2,sum3,sum4,sum5;
    scanf("%lf %lf %lf",&a,&b,&c);
    sum1=(a*c)/2;
    sum2=pai*c*c;
    sum3=((a+b)/2)*c;
    sum4=b*b;
    sum5=a*b;
    printf("TRIANGULO: %.3lf\nCIRCULO: %.3lf\nTRAPEZIO: %.3lf\nQUADRADO: %.3lf\nRETANGULO: %.3lf\n",sum1,sum2,sum3,sum4,sum5);
    return 0;
}
