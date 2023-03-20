n,m,s=list(map(int,input().split()))
x=[]
y=[]
for i in range(n):
    xx=list(input())
    x.append(xx)
h=list(map(int,input().split()))
for i in h:
    if i==-1:
        exit(0)
    if len(y)==s and i!=0:
        print(y.pop(),end="")
        y.append(x[i-1].pop(0))
    elif i==0 and y!=[]:
        print(y.pop(),end="")
    else:
        y.append(x[i-1].pop(0))