#include<stdio.h>
int main()
{
    double n;
    int con,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12;
    int rem,rem1,rem2,rem3,rem4,rem5,rem6,rem7,rem8,rem9,rem10;
    scanf("%lf",&n);
    printf("NOTAS:\n");

    con=n*100;
    v1=con/10000;
    printf("%d nota(s) de R$ 100.00\n",v1);
    rem=con%10000;

    v2=rem/5000;
    printf("%d nota(s) de R$ 50.00\n",v2);
    rem1=rem%5000;

    v3=rem1/2000;
    printf("%d nota(s) de R$ 20.00\n",v3);
    rem2=rem1%2000;

    v4=rem2/1000;
    printf("%d nota(s) de R$ 10.00\n",v4);
    rem3=rem2%1000;

    v5=rem3/500;
    printf("%d nota(s) de R$ 5.00\n",v5);
    rem4=rem3%500;

    v6=rem4/200;
    printf("%d nota(s) de R$ 2.00\n",v6);
    printf("MOEDAS:\n");
    rem5=rem4%200;

    v7=rem5/100;
    printf("%d moeda(s) de R$ 1.00\n",v7);
    rem6=rem5%100;

    v8=rem6/50;
    printf("%d moeda(s) de R$ 0.50\n",v8);
    rem7=rem6%50;

    v9=rem7/25;
    printf("%d moeda(s) de R$ 0.25\n",v9);
    rem8=rem7%25;

    v10=rem8/10;
    printf("%d moeda(s) de R$ 0.10\n",v10);
    rem9=rem8%10;

    v11=rem9/5;
    printf("%d moeda(s) de R$ 0.05\n",v11);
    rem10=rem9%5;

    v12=rem10/1;
    printf("%d moeda(s) de R$ 0.01\n",v12);
    return 0;
}
