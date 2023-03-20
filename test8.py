s=[]
n=0
for i in range(1,10):
    for j in range(1,10):
        k=i*j
        if k not in s:
            s.append(k)
            n+=1
print(n)
s.sort()
for i in range(0,len(s)):
    print(s[i],end=",")
    if (i+1)%10==0:
        print()