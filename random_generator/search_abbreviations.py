from datasets import load_dataset
import random
import re
d=load_dataset("wikipedia", "20220301.en", split="train")
f2 = open("abbreviations.txt", "w")
word_count = {}

"""
dict word_count = {"word":[a, b, c], ....}
a = word without following period
b = word with following period
c = word with following period with non lower char (end of sentence pattern)

pattern for an acronym, title, and regular word
< = small #, > = big #

    U.S.A | Mr | the
a =   <   | <  |  >
b =   >   | >  |  <
c =   >   | <  |  <

Titles like Mr. should be detected so they are not treated like a sentence,
although they have the same structure as the end of sentence that can't be identified w/ a pattern.
If they are constantly followed by a period and capital, they aren't part of regular sentence ending.
"""
def count_words(article):
	article = re.sub(r'[^A-Z^a-z^0-9^\.]', ' ', article)
	# count for word without period at the end
	for word in article.split():
		if word[len(word)-1] != ".":
			if word not in word_count:
				# each key has value of a three number list
				word_count[word] = [1, 0, 0]
			else:
                # first number counts the word without a period at the end (ex. 'Mr', 'cat', 'U.S.A')
				word_count[word][0] += 1
	for word in article.split():
		if word[len(word)-1] == ".":
			if word[:len(word) - 1] not in word_count:
				word_count[word[:len(word) - 1]] = [0, 1, 0]
			else:
                # second number counts the word with period at the end (ex. 'Mr.', 'cat.', 'U.S.A.')
				word_count[word[:len(word) - 1]][1] += 1
    # pattern for the end of a sentence, word + period + space + a non lowercase character (ex. 'Mr. A', 'cat. M', 'U.S.A. J')
	sentence_pattern = re.compile(r'[^n^\s]+?\.\s+[^a-z]')
	sentence_matches = list(sentence_pattern.finditer(article))
	for match in sentence_matches:
		match = match.group()
		match = match[:-1].strip().strip(".")
        # third number count the word at the end of a sentence pattern
		if match in word_count:
			word_count[match][2] += 1

# number of sentences in sample size

def generate_abbreviations(random_index):
	# random_index = 36000
	for article in d:
		if random.randint(0,6400000) < random_index:
			count_words(article["text"])
	for key in word_count:
		if (word_count[key][0] + word_count[key][1] >= random_index/1000 and word_count[key][1] > (word_count[key][1] + word_count[key][0]) * 0.75 
			and word_count[key][2] > word_count[key][1] * 0.75 and abs(word_count[key][1] - word_count[key][2]) > 1 and len(key) < 7):
			f2.write(str(key) + "\n") 
	f2.close()