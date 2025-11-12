#include<stdio.h>
int main()
{
    double a,b,c,d,X,Y;
    scanf("%lf %lf %lf %lf",&a,&b,&c,&d);
    X=((a-c)*(a-c))+((b-d)*(b-d));
    Y= sqrt(X);
    printf("%.4lf\n",Y);
    return 0;
}
