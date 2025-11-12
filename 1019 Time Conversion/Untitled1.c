#include<stdio.h>
int main()
{
    int N,h,m,s,rem;
    scanf("%d",&N);
    h=N/(60*60);
    rem=N%(60*60);
    m=rem/60;
    rem=rem%60;
    s=rem%60;
    printf("%d:%d:%d\n",h,m,s);
    return 0;
}
