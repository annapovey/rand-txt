from datasets import load_dataset
import random
import re
d=load_dataset("wikipedia", "20220301.en", split="train")
f = open("wikipedia_20220301_en_train.txt", "w")
f2 = open("abbreviations.txt", "r")

two_sent_per_line = False
random_probability = 72000
if two_sent_per_line:
	number = 0
abbreviations = f2.read().split()
print(len(d))
for article in d:
	if random.randint(0,6458670) < random_probability:
		# sentence pattern: period + space + [capital + contents(minimum seven characters)(not greedy) 
		#				    + period] + space + captial
		sentence_pattern = re.compile(r'\.\s+[A-Z][^\n]{7,}?\s?\"?\)?\.\"?\)?\s+[^a-z]')
		word_list = article["text"].split(" ")
		word_dict = {}
		# An issue with wikipedia article formatting are random periods with spaces before them:
		# ex. The outlying islands of Italy make up an official region of Insular Italy with an area of .
		# These aren't detected as sentences but can be appended to the following sentence, so they're removed.
		article["text"] = re.sub(r'\.\s+[A-Z][^\n]{7,}?\s\.\s+[^a-z]', '', article["text"])
		# finds sentence matches in article
		sentence_matches = list(sentence_pattern.finditer(article["text"]))
		if len(sentence_matches) == 0:
			random_probability += 1
		else:
			two_sentence_pattern = re.compile(r'\.\s+[A-Z][^\n]{7,}?\s?\"?\)?\.\"?\)?\s+[^a-z]')
			# randomly selects sentence in the range of the sentence list
			match = sentence_matches[random.randint(0, len(sentence_matches)-1)].group()[2:-1].strip()
			match_words = match.split()
			match_last = match_words[len(match_words) - 1]
			# makes sure the text isn't from parenthesis or quote
			if match.count(")") != match.count("(") or match.count("\"")%2 == 1 or match.count(" ") == 1:
				random_probability += 1
			elif len(list(two_sentence_pattern.finditer(match))) >= 1:
				random_probability += 1
			elif len(re.findall(r'[A-Z0-9][^A-Z]', match)) >= match.count(" "):
				random_probability += 1
			elif len(match_last) < 7:
				for abb in abbreviations:
					if(match_last == abb):
						random_probability += 1
			else:
				f.write(match)
				f.write("\n")
				if two_sent_per_line:
					number+=1
					if number%2 == 0:
						f.write("\n")
					else:
						f.write(" ")
f.close()
