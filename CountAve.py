a=0
count=0
while(True):
    x = input()
    if x == 0:
        break
    a += x
    count += 1
print('a = ',a)
print('count = ',count)
print('ave = ',a/count)
