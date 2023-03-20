def t(x):
    if x%2==0:
        x/=2
    else:
        x=(3*x+1)/2
    return x
n=int(input())
s=map(int,input().split())
s=list(s)
ss=s[0:]
for i in s:
    j=i
    while j>1:
        j=t(j)
        if j in ss:
            ss.remove(j)
ss.sort(reverse=True)
for i in ss:
    if not i == ss[len(ss)-1]:
        print(i,end=" ")
    else:
        print(i)