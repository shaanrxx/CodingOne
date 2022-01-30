## Week 8

# spell checker

def readDictionaryFile(dictionaryFilename):
    dictionaryWords = []
    inputFile = open(dictionaryFilename, "r")
    for line in inputFile:
        word = line.strip()
        dictionaryWords.append(word)
    inputFile.close()
    return dictionaryWords


def readTextFile(textFilename):
    words = []
    inputFile = open(textFilename, "r")
    for line in inputFile:
        wordsOnLine = line.strip().split()
        for word in wordsOnLine:
            words.append(word.strip(".,!\":;?").lower())
    inputFile.close()
    return words


def findErrors(dictionaryWords, textWords):
    misspelledWords = []
    for word in textWords:
        if word not in dictionaryWords:
            misspelledWords.append(word)
    return misspelledWords

def printErrors(errorList):
    print("The misspelled words are: ")
    for word in errorList:
        print(word)

def main():
    print("Welcome to the spell checker")
    dictionaryFile = input("Please enter the dictionary file: ")
    textFile = input("Please enter the text file: ")
    dictionaryList = readDictionaryFile(dictionaryFile)
    textList = readTextFile(textFile)
    errorList = findErrors(dictionaryList, textList)
    printErrors(errorList)


main()