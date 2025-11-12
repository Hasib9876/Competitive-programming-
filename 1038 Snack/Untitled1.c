#include<stdio.h>
int main()
{
    double a,y,z;
    scanf("%lf %lf",&a,&y);
    if(a==1)
    {
        z=4.00*y;
        printf("Total: R$ %.2lf\n",z);
    }
    else if(a==2)
    {
        z=4.50*y;
        printf("Total: R$ %.2lf\n",z);
    }
    else if(a==3)
    {
        z=5.00*y;
        printf("Total: R$ %.2lf\n",z);
    }
    else if(a==4)
    {
        z=2.00*y;
        printf("Total: R$ %.2lf\n",z);
    }
    else if(a==5)
    {
        z=1.50*y;
        printf("Total: R$ %.2lf\n",z);
    }
    return 0;
}
