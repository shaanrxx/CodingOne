## Week 5
## Make a program that uses a lookup table to convert any set of alphabets into their corresponding NATO phonetic alphabets. 
## Also implement the inverse function

nato = {'A':'Alpha', 'B':'Bravo','C':'Charlie', 'D':'Delta', 'E':'Echo', 'F':'Foxtrot', 'G':'Golf', 'I':'India', 'J':'Juliet', 'K':'Kilo', 'L':'Lima', 'M':'Mike', 'N':'November', 'O':'Oscar', 'P':'Papa', 'Q':'Quebec', 'R':'Romeo', 'S':'Sierra', 'T':'Tango', 'U':'Uniform', 'V':'Victor', 'W':'Whiskey', 'X':'X-ray', 'Y':'Yankee', 'Z':'Zulu'}

word = input('Enter word:')
for letter in word:
   print(nato.get(letter.upper()))