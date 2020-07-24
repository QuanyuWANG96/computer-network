# a = {10:3,2:4}
# for i in list(a.items()):
#     if not i in a:
#         print(i)
# from os import path
#
# p = path.join('/etc', 'sysconfig', 'network')  # 根据不同的系统，将每个字符串组合成路径形式
# print(type(p), p)
# id = 1
# pp = 'a_'+ str(id)+'.out'
# f = open(pp,'a')
# f.write("hello")
# f.close()




#
# a =[[1,2,3], [2,3,4], [4,5,6]]
# b=[[1,2,3]]
# c = a[:]
# for i, j, k in a:
#     if [i, j,k] not in b:
#         print("zzzzz")
#         print(str(i) + " " + str(j) + " " + str(k))
#         b.append([i, j, k])
#     c.remove([i,j,k])
# a = c[:]
# # a.clear()
# # print("dddddd")
# # print(b)
# print(a)
# print(c)

a = set()
a.add((1,2,3))
a.add((2,4,5))
print(a)
for i, j ,k in a:
    print(str(i) + " " + str(j) + " " + str(k))
if (4,5,6) not in a:
    print("aaaaaaaaaaa")