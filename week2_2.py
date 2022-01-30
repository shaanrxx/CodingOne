

# Python3 implementation of the approach
alphabet = 26
 
# Function to print the frequency
# of each of the characters of
# s in alphabetical order
def compressString(s, n) :
 
    # To store the frequency
    # of the characters
    freq = [ 0 ] * alphabet
 
    # Update the frequency array
    for i in range(n) :
        freq[ord(s[i]) - ord('a')] += 1
 
    # Print the frequency in alphatecial order
    for i in range(alphabet.lower()) :
 
        # If the current alphabet doesn't
        # appear in the string
        if (freq[i] == 0) :
            continue
 
        print((chr)(i + ord('a')),freq[i],end = " ")
 
# Driver code
if __name__ == "__main__" :
 
    s = input("write something ")
    n = len(s)
 
    compressString(s, n)
 