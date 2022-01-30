## Week 4 part 2

## Start with 4 words “comfortable”, “round”, “support”, “machinery”, return a list of all possible 2 word combinations.
##  Example: ["comfortable round", "comfortable support", "comfortable machinery", .....]


def word_variations(word_list):
  combinations = []
  for first_word in word_list:
    for second_word in word_list:
      if first_word != second_word:
        combinations.append(f'{first_word}, {second_word}')

  return combinations

word_list = ["comfortable", "round", "support", "machinery"]
print(word_variations(word_list))