#python program to see if a number is odd or even


num = int(input("Enter a number: "))
if (num % 2) == 0:
    print("{0} is Even".format(num))
elif (num % 2) == 1:
    print("{0} is Odd".format(num))
else:
    print("Number is neither even or odd, please try again")
