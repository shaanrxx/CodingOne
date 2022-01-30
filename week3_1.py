#week 3

#Make a function that takes two arguments (given name and family name), the second of which is optional.
#  Print a greeting according to which arguments are provided.


firstname=input("What is your first name: ")
question=input("would you like to say your last name? Y for yes, N for No")

if question == "Y":
    lastname=input("What is your family name: ")
    print("Hello" + " " + firstname + " " + lastname)
elif question == "N":
    print("Hello" + " " + firstname)
else:
    print("Please try again")








