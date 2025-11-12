#include<stdio.h>
int main()
{
    float a,b,c,i,j,k,l;
    scanf("%f %f %f",&a,&b,&c);
    i=a+b;
    j=b+c;
    k=c+a;
    if(a<j && b<k && c<i) printf("Perimetro = %.1f\n",a+b+c);
    else
    {
        l=(a+b)*c;
        printf("Area = %.1f\n",l/2);
    }
    return 0;
}
