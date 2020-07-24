import re
s  = ["a","b"]
s = str(s)
print(s)
# s = s[1:-1].split("\"")
s = re.split(r"[,\s\"]", s[1:-1])
# print(s[1:-1])
print(s)
for i in range(len(s)):
    if s[i] is not '':
        print(s[i].strip('\''))

# print(re.split(r"[,\"]", s[1:-1]))
