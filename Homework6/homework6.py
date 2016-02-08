from nltk.tokenize.api import StringTokenizer
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from re import match

# returns list of strings that dosen't include any stopword
def filter_stopwords(sent, stopwords) :
	tokenizer = StringTokenizer()
	tokenizer._string = ' '
#	tokenizer = StanfordTokenizer()
#	try :
#		tokens = word_tokenize(sent)
#	except :
# when I use better tokenizer, number of whole words aren't over 10,000
	tokens = tokenizer.tokenize(sent)
#	print tokens
	words = []
	for token in tokens :
		if not token.lower() in stopwords :
			words.append(token)
	return words

# returns list of strings those are consist of stems
def do_stemming(words) :
	stemmer = PorterStemmer()
	def stem(word) :
		try :
			return stemmer.stem(word)
		except :
			return word
	return [stem(word) for word in words]

# returns P(xi/spam), P(xi/ham) for any xi
def train(smses, classes) :
	spam = {'UNKNOWN' : 0, 'PHONE_NUMBER' : 0, 'URL' : 0}
	ham = {'UNKNOWN' : 0, 'PHONE_NUMBER' : 0, 'URL' : 0}
	length = len(smses)
	assert(length == len(classes))
	for i in range(len(smses)) :
		for word in smses[i] :
			low = word.lower()
			if classes[i] == 'spam' :
				C = spam
			else :
				C = ham
			if match(phone_number, low) :
				C['PHONE_NUMBER'] += 1
			elif match(url, low):
				C['URL'] += 1
			elif not low in vocabulary :
				C['UNKNOWN'] += 1
			elif low in C :
				C[low] += 1
			else :
				C[low] = 1
	return spam, ham

# returns P(spam|X) > P(ham|X)
def classify(sent) :
	sms = do_stemming(filter_stopwords(sent.strip(), stopwords))
	# P(spam|X) = P(X|spam) * P(spam) / P(X)
	Pspam = 1
	Pham = 1
	for word in sms :
		low = word.lower()
		if match(phone_number, low) :
			Pspam *= float(spam['PHONE_NUMBER'])/vocabulary['PHONE_NUMBER']
			Pham *= float(ham['PHONE_NUMBER'])/vocabulary['PHONE_NUMBER']
		elif match(url, low) :
			Pspam *= float(spam['URL'])/vocabulary['URL']
			Pham *= float(ham['URL'])/vocabulary['URL']
		else :
			if low in spam :
				Pspam *= float(spam[low])/vocabulary[low]
			elif low in ham :
				Pham *= float(ham[low])/vocabulary[low]
			else :
				Pspam *= float(spam['UNKNOWN'])/vocabulary['UNKNOWN']
				Pham *= float(ham['UNKNOWN'])/vocabulary['UNKNOWN']
	return (Pspam > Pham)

if __name__ == "__main__" :
	stopwords_str = open("stopwords.txt", 'r').readline()
	words_str = stopwords_str.replace("\"","").strip()
	stopwords = words_str.split(',')

#	print stopwords
#	words = filter_stopwords(sentence, stopwords)
#	print do_stemming(words)

	classes = []
	smses = []
	total_voca = 0
	total_ham = 0
	total_spam = 0
	train_file = open("train", 'r')

	# before inserting, gets P(spam), P(ham)
	for line in train_file :
		index = line.index('|')
		CLASS, sent = line[:index], line[index+1:]
		classes.append(CLASS)
		SMS = do_stemming(filter_stopwords(sent.strip(), stopwords))
		smses.append(SMS)
		for word in SMS :
			total_voca += 1
			if CLASS == 'spam' :
				total_spam += 1
			elif CLASS == 'ham' :
				total_ham += 1

	number_words = {'PHONE_NUMBER' : 0, 'URL' : 0}
	### phonenumber - http://www.regexr.com/38pvb
	### ^\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*$
	phone_number = '\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*'
	### url
	url = '\s*((https?|ftp)://)|(\.com)|(\.net)|(www\.)\s*'

	# according to all words, gets {whole word : frequency} dictionary
	for sms in smses :
		for word in sms :
			low = word.lower()
			if match(phone_number, low) :
				number_words['PHONE_NUMBER'] += 1
			elif match(url, low):
				number_words['URL'] += 1
			elif low in number_words :
				number_words[low] += 1
			else :
				number_words[low] = 1

	items = sorted(number_words.items(), key = lambda item : item[1])
#	print items, len(items)

	# cuts top 10,000 frequent words
	total_UNKNOWN = 0
	for item in items[:-10000] :
		total_UNKNOWN += item[1]
	voca_item = items[-10000:] + [(u'UNKNOWN', total_UNKNOWN)]

	vocabulary = {}
	for item in voca_item :
		vocabulary[item[0]] = item[1]
#	print vocabulary, len(vocabulary)	
	
	spam, ham = train(smses, classes)
		
#	sentence = "Hello, My name is Jaryong Lee. I like playing soccer"
#	classify(sentence)


	# gets TP, TN, FP, FN by numbers (not probability)
	TP, TN, FP, FN = 0, 0, 0, 0
	test_file = open("test", 'r')
	for line in test_file :
		index = line.index('|')
		CLASS, sent = line[:index], line[index+1:]
		CONDITION = (CLASS == 'spam')
		PREDICTION = classify(sent)
#		print CONDITION, PREDICTION
		if CONDITION and PREDICTION :
			TP += 1
		elif CONDITION and not PREDICTION :
			FN += 1
		elif not CONDITION and PREDICTION :
			FT += 1
		elif not CONDITION and not PREDICTION :
			TN += 1
			
	print '\tCondition\nPredi\t%4d%4d\nction\t%4d%4d' %(TP, FP, FN, TN)

	# Precision = tp/(tp + fp)
	# Recall = tp/(tp + fn)
	# F-measure = 2*precision*recall/(precision + recall)
	P = float(TP)/(TP + FP)
	R = float(TP)/(TP + FN)
	F = 2*P*R/(P+R)
	print 'Precision: %g\nRecall: %g\nF-measure: %g' %(P, R, F)
