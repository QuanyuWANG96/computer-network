a =[[1,2,3], [2,3,4], [4,5,6]]
b=[[1,2,3]]
# c = a[:]
for i, j, k in a:

    if [i, j,k] not in b:
        print("zzzzz")
        print(str(i) + " " + str(j) + " " + str(k))
        b.append([i, j, k])
        # c.remove([i,j,k])
# a = c[:]
a.clear()
print("dddddd")
print(b)
print(a)
# print(c)