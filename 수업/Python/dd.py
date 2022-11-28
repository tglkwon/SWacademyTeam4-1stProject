i = 0
a = lambda x:x+i
i = 1
b = lambda x:x+i
i = 2
c = lambda x:x+i
i = 3
d = lambda x:x+i
i = 4
e = lambda x:x+i
t = (a,b,c,d,e)

print(t[0](3), t[3](3))
print(id(t[0]), id(t[4]))