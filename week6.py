# Set initial state of l-system
initial = "AB"

# Rules for the l-system
rules = {
	"A": "AB",
	"B": "A"
}

def l_system(initial, rules, generation):   #function and calls rules and initial variables
	current = initial                 #defines variable

	for _ in range(0, generation):     #loops through the possibilities
		result = ""                  #stores the result

		for state in current:               #loops through initial
			result += rules.get(state, state)      #result adds the rules list and prints out them twice

		current = result          ##the variable has changes to stroe the new result

	return current              # returns the result and end the function

for i in range(0, 10):                       #loop 1 -10
	print( "{}: {}".format(i, l_system(initial, rules, i)) )     #prints the result of l system
	
