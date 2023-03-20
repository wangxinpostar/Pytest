c = 0
for i in range(1, 1817):
    s = str(i**3)
    L = list(map(int, s))
    if i == sum(L):
        c = c+1
print(c)