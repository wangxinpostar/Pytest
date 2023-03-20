s=input()
zi=[]
wen=[]
ying=[]
notdaxiao=[]
a,b,c,d=0,0,0,0
for i in s:
    if i not in zi:
        zi.append(i)
        a+=1
    if '\u4e00'<i<'\u9fff' or 'a'<=i<='z' or 'A'<=i<='Z'  :
        if i not in wen:
            wen.append(i)
            b+=1
    if ('a'<=i<='z' or 'A'<=i<='Z' )and i not in ying:
        ying.append(i)
        c+=1
    if 'a'<=i<='z' or 'A'<=i<='Z' :
        if i.upper() not in notdaxiao:
            notdaxiao.append(i.upper())
            d+=1
print("不重复的字符共有{}个。他们是：".format(a))
print(zi)
print("不重复的字符或文字共有{}个。他们是：".format(b))
print(wen)
print("不重复的英文字符共有{}个。他们是".format(c))
print(ying)
print("不重复的英文字符（不区分大小写）共有{}个。他们是".format(d))
print(notdaxiao)


    
