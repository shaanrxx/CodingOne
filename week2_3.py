num = int(input("enter a number: "))
num2 = int(input("what number do you want this number to be divided by: "))



count = 0

while num >= num2:
    num = num - num2
    count = count + 1
    
    #return count

print("the number is " + str(count) + " with a remainder of " + str(num))



