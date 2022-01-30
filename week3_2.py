## Week 3

## Write a function that takes in any English word and turns it into pig latin. 
##Extra if you can write another function that converts a whole sentence


def char_Vowel(v):
    vowel = ["A","E","I","O","U", "a","e","i","o","u" ]
    if v in vowel:
        return True
    else:
        return False
    
def pigLatin(s):
    flag = False;
    vowel_index = 0
    for i in range(len(s)):
        if(char_Vowel(s[i])):
            vowel_index = i
            flag = True;
            break;
    if (not flag):
        return s;
    pigLatin = s[vowel_index: ] + s[0:vowel_index] + "ay"
    return pigLatin

phrase = input("enter a word or sentence: ")
list = phrase.split()

print("The original phrase  is ")
print(phrase)

pig_str = ""

for word in list:
    pig_str += " " + pigLatin(word)

print("The Pig latin is: ")
print(pig_str)