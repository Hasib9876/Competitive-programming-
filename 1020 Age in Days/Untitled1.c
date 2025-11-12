#include<stdio.h>
int main()
{
    int N,y,m,rem;
    scanf("%d",&N);
    y=N/365;
    rem=N%365;
    m=rem/30;
    rem=rem%30;
    printf("%d ano(s)\n%d mes(es)\n%d dia(s)\n",y,m,rem);
    return 0;
}
