#include<stdio.h>
int main()
{
    float slr,nslr;
    char x='%';
    scanf("%f",&slr);
    if(slr<=400)
    {
        nslr=slr+(slr*.15);
        printf("Novo salario: %.2f\n",nslr);
        printf("Reajuste ganho: %.2f\n",slr*.15);
        printf("Em percentual: 15 %c\n",x);
    }
    else if(slr>400 && slr<=800)
    {
        nslr=slr+(slr*.12);
        printf("Novo salario: %.2f\n",nslr);
        printf("Reajuste ganho: %.2f\n",slr*.12);
        printf("Em percentual: 12 %c\n",x);
    }
    else if(slr>800 && slr<=1200)
    {
        nslr=slr+(slr*.10);
        printf("Novo salario: %.2f\n",nslr);
        printf("Reajuste ganho: %.2f\n",slr*.10);
        printf("Em percentual: 10 %c\n",x);
    }
    else if(slr>1200 && slr<=2000)
    {
        nslr=slr+(slr*.07);
        printf("Novo salario: %.2f\n",nslr);
        printf("Reajuste ganho: %.2f\n",slr*.07);
        printf("Em percentual: 7 %c\n",x);
    }
    else if(slr>2000)
    {
        nslr=slr+(slr*.04);
        printf("Novo salario: %.2f\n",nslr);
        printf("Reajuste ganho: %.2f\n",slr*.04);
        printf("Em percentual: 4 %c\n",x);
    }
    return 0;
}
