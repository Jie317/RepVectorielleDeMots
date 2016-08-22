import sys
import nltk.data
import os

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

inputpath=sys.argv[1]
outputpath=sys.argv[2]

i = 0
with open(inputpath,'r') as corpus, open(outputpath,'w+') as output:
	for line in corpus:
		for sentence in sent_detector.tokenize(line.strip().decode("utf8")):
			output.write(sentence.encode('utf-8')+'\n')
			i += 1
		
		if i%1000000 <= 20:
			print '>>>> Finished sentences: ',i
		

