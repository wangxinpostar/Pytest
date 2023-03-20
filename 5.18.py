import os

# def mkdir(path):
#     folder = os.path.exists(path)
#     if not folder:                  
#         os.makedirs(path)
#         print("D:\works文件夹已创建")


# def check(n):
#     if n<0 or n>100:
#         raise ValueError


# mkdir("D:\works")
# with open('D:\works/'"score"+'.txt',"a") as w:
#     n=int(input("请输入评委人数："))
#     w.write("{}\n".format(n))
#     i=1
#     while(i<=n):
#         try:
#             m=int(input("请输入第{}个评委评分".format(i)))
#             check(m)
#         except ValueError:
#             print("输入非法，请重输！")
#         else:
#             w.write("{}\n".format(m))
#             i+=1

list1=[];num=0
with open('D:\works\score.txt',"r") as w:
    list1=w.readlines()

n=int(list1[0])
for i in range(1,n+1):
    num+=int(list1[i])

list2=sorted(list1[1:],reverse=True)
num-=int(list2.pop(0))+int(list2.pop())
num/=n-2

list2.insert(0,"{}\n".format(n-2))
list2.insert(1,"{}\n".format(num))

with open('D:\works\score.txt',"w") as w:
    for i in list2:
        w.write(i)