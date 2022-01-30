## Week 5 part 2

## Implement a Caesar Cipher function that takes a string and shift amount, outputs the encrypted string.

def encripted(string, shift):
    cipher=''
    for char in string:
        if char==' ':
            cipher = cipher + char
        elif char.isupper():
            cipher = cipher + chr((ord(char) + shift - 65) % 26 + 65)
        else:
            cipher = cipher + chr((ord(char) + shift - 97) % 26 + 97)
    return cipher

text = input("enter the text: ")
s = int(input("enter the shift key: "))
print("the orginal string is: ", text)
print("the encripted message is: ", encripted(text, s))