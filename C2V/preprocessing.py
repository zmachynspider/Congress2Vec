from nltk.corpus import stopwords
from collections import Counter
import string

def strip_stopwords(text):
	'''Ingests a string of text and removes stopwords from the string'''
	return ' '.join([word for word in text.split() if word not in stopwords.words('english')])

def tokenize(text, strip_stopwords=True):
    '''Given a string of text, breaks up the text into a list of lowercase words'''
    if strip_stopwords:
        text = strip_stopwords(text)
    return text.translate({ord(c): None for c in string.punctuation}).lower().split()

def stemmatize(text, stemmer, strip_stopwords=True):
    '''Given a string of text, returns a list of stems. Defaults to English SnowballStemmer'''
    if strip_stopwords:
        text = strip_stopwords(text)
    text = text.translate({ord(c): None for c in string.punctuation})
    return [stemmer.stem(word) for word in text.split()]

def lemmatize(text, lemmer, strip_stopwords=True):
    '''Given a string of text, returns a list of lems'''
    if strip_stopwords:
        text = strip_stopwords(text)
    text = text.translate({ord(c): None for c in string.punctuation})  
    return [lemmer.lemmatize(x[0]).lower() for x in pos_tag(word_tokenize(text))]

def get_haps(list_of_docs):
	'''Given a list of documents which contain a list of words, identifies the haplaxes in the docsc'''
	vocab = Counter()
	for doc in list_of_docs:
		vocab += Counter(doc)
	return [k for k, v in vocab.items() if v == 1]    

def get_vocab(list_of_docs):
	'''Given a list of documents which contain a list of words, returns a Counter object of Vocab'''
	vocab = Counter()
	for doc in list_of_docs:
		vocab += Counter(doc)
	return vocab  	

def findTParty(name, t_party, party):
    '''Function estimates if the member belongs to the tea party. Only approximately correct 
    this is why we also use a hueristic of checking whether they belong to the Republican 
    party as a santiy check'''
    if any(t in name for t in t_party) and (party != '(D)'):
        return True
    else:
        return False