#include<stdio.h>
int main()
{
    int ih,im,fh,fm,m;
    scanf("%d %d %d %d",&ih,&im,&fh,&fm);
    if(im>fm)
    {
        m=(fm+60)-im;
        if(ih==fh)printf("O JOGO DUROU 24 HORA(S) E %d MINUTO(S)\n",m);
        else if(ih>fh) printf("O JOGO DUROU %d HORA(S) E %d MINUTO(S)\n",(fh+24)-ih-1,m);
        else printf("O JOGO DUROU %d HORA(S) E %d MINUTO(S)\n",fh-ih-1,m);
    }
    else
    {
        if(fm>im) m=fm-im;
        else  m=0;
        if(ih==fh) printf("O JOGO DUROU 24 HORA(S) E %d MINUTO(S)\n",m);
        else if(ih>fh) printf("O JOGO DUROU %d HORA(S) E %d MINUTO(S)\n",(fh+24)-ih,m);
        else printf("O JOGO DUROU %d HORA(S) E %d MINUTO(S)\n",fh-ih,m);
    }
    return 0;
}
