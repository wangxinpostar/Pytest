import itertools
n=[1,2,4,6,8,0]
s=[]
ans=0
k=0
for i in itertools.permutations(n,4):
    if i[0]!=0:
        s.append(i)
        ans+=1
print(ans)
for i in s:
    print("{}{}{}{},".format(i[0],i[1],i[2],i[3]),end="")
    k+=1
    if k%10==0:
        print("\n")