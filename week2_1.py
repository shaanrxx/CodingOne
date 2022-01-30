a = int(input("Pick a number1: "))
b = int(input("Pick a number2: "))
c = int(input("Pick a number3: "))
d = 0

for i in range(a, b):
    if(i % c)==0:
        d = d + i

print(d)