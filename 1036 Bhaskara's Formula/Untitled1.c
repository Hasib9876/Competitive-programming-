#include<stdio.h>
#include<math.h>
int main()
{
    double a,b,c,avg,r1,r2;
    scanf("%lf %lf %lf",&a,&b,&c);
    avg=(b*b)-(4*a*c);
    if(avg>=0 && a!=0)
    {
        r1=(-b+sqrt(avg))/(2*a);
        r2=(-b-sqrt(avg))/(2*a);
        printf("R1 = %.5lf\nR2 = %.5lf\n",r1,r2);
    }
    else printf("Impossivel calcular\n");
    return 0;
}
