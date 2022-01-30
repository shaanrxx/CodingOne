## Week 4 part 1

## Write a program that given a list of numbers, multiply all numbers in the list. Bonus for ignoring non-number element.
## Example: input: [1, 2, 3, 4], output: 24

try:
    num1 = int(input("Enter a number: "))
    num2 = int(input("Enter a number: "))
    num3 = int(input("Enter a number: "))
    num4 = int(input("Enter a number: "))
except ValueError as e:
    print("NOT VALID")

list = [num1, num2, num3, num4]
result=1

def multiplyList(list) :
     
    # Multiply elements one by one
    result = 1
    for x in list:
         result = result * x
    return result

print(multiplyList(list))