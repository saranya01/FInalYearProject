#Author :Kalyan Pichumani and Saranya Nagarajan 
#http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
#This program will predicts the sentiment of every tweet in the database and stores the sentiment as a new attribute in  the database
#Run this program python sentiment2.py 

import goslate
import couchdb
import re
import csv
import urllib
from textblob import TextBlob
import svmutil
import nltk
from svmutil import *
#start featureExtraction

def featureExtraction(tweet):
    tokens = set(tweet)
    features = {}
    for each in featureList:
        features['contains(%s)' % each] = (each in tokens)
    return features
#end

#start getfeatureVector
def getFeatureVector(tweet,stopwrds):
	featureVector = []
	#split tweet into tokens
	tokens = tweet.split()
	for w in tokens:
		#replace two or more with two occurrences
		w = moreThanOneWord(w)
		#strip punctuation
		w = w.strip('\'"?,.')
		#check if the word stats with an alphabet
		value = re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', w)
		regax = re.compile(r'/[ \t]+/')
		result = regax.match(w)
		#ignore if it is a stop word
		#print 
		if(w in stopwrds or value is None):
			continue
		else:
		    if(result != None):
			regax = re.compile(r'/[ \t]+/')
                	result = regax.match(w)
			featureVector.append(result.lower())
			print result
		    else:	
			featureVector.append(w.lower())
	return featureVector
#end

#start moreThanOneWord
def moreThanOneWord(s):
    #look for 2 or more repetitions of character and replace with the character itself
    regax = re.compile(r'(.)\1{1,}', re.DOTALL)
    return regax.sub(r'\1\1', s)
#end


def getSVMFeatureVectorAndLabels(tweets, featureList):
    sortedFeatures = sorted(featureList)
   # sortedFeatures = featureList
    map = {}
    feature_vector = []
    labels = []
    for t in tweets:
        label = 0
        map = {}
        #Initialize empty map
        for w in sortedFeatures:
            map[w] = 0

        tweetToken = t[0]
        tweetSentiment = t[1]
        #Fill the map
        for word in tweetToken:
            #process the word (remove repetitions and punctuations)
            word = moreThanOneWord(word)
            word = word.strip('\'"?,.')
            #set map[word] to 1 if word exists
            if word in map:
                map[word] = 1
        #end for loop
        values = map.values()
        feature_vector.append(values)
        if(tweetSentiment == 'positive'):
            label = 0
        elif(tweetSentiment == 'negative'):
            label = 1
        elif(tweetSentiment == 'neutral'):
            label = 2
        labels.append(label)
		
    
	#return the list of feature_vector and labels
	return {'feature_vector' : feature_vector, 'labels': labels}
#end

#start stopWordList
def stopWordList(fileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fStopList = open(fileName, 'r')
    line = fStopList.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fStopList.readline()
    fStopList.close()
    return stopWords
#end


def getSVMFeatureVector(test_tweets, featureList):
    sortedFeatures = sorted(featureList)
    map = {}
    feature_vector = []
    for t in test_tweets:
        map = {}
        #Initialize empty map
        for w in sortedFeatures:
            map[w] = 0

        tweetToken = t
        #tweetSentiment = t[1]
        #Fill the map
        for word in tweetToken:
            #process the word (remove repetitions and punctuations)
            word = moreThanOneWord(word)
            word = word.strip('\'"?,.')
            #set map[word] to 1 if word exists
            if word in map:
                map[word] = 1
        #end for loop
        values = map.values()
        feature_vector.append(values)
        
    #return the list of feature_vector and labels
    return feature_vector
#end


try:
	ffv = open('FeatureVectorSVM.txt', 'w')
except IOError, message:  # file open failed
	print "File could not be opened:", message
	sys.exit(1)
	
 
try:
	fts = open('TrainingSetSVM.txt', 'w')
except IOError, message:  # file open failed
	print "File could not be opened:", message
	sys.exit(1)


stopWords = []	
st = open('StopWords.txt', 'r')
stopWords = stopWordList('StopWords.txt')
db = couchdb.Database('http://localhost:5984/time')
rows = db.view('_all_docs', include_docs = True)
counter = 0;
inpTweets = csv.reader(open('mycsv.csv',"rU"), dialect='excel-tab') 
outTweet = csv.writer(open('TestResultSVM.csv',"wb"), dialect='excel-tab')
featureList = []
tweets = []
for each in inpTweets:
	sentiment = each[0]
	tweet = each[1]
	featureVector = getFeatureVector(tweet,stopWords)
	print >> ffv, featureVector
	featureList.extend(featureVector)
	tweets.append((featureVector, sentiment));
	
#Train the classifier
result = getSVMFeatureVectorAndLabels(tweets, featureList)
problem = svm_problem(result['labels'], result['feature_vector'])
#'-q' option suppress console output
param = svm_parameter('-q')
param.kernel_type = LINEAR
classifier = svm_train(problem, param)
#svm_save_model(classifierDumpFile, classifier)
print tweets
print >> fts, result	
# Remove featureList duplicates
featureList = list(set(featureList))

fts.close()
fact = open("test.txt","w")
# Test the classifier
fact1 = open("test1.csv","w")
doc2=[]
test_tweets =[]
test_tweets1 = []
docs = [row.doc for row in rows]
i = 0
a = []
print len(docs)
#Takes every tweet individually and marks the sentiment
while ( i < len(docs) ):
 	    	line = docs[i]["translated_text"]
	    	t=line.encode("utf-8")
	    	doc2.append(t)	
	    	featureVector = getFeatureVector(t,stopWords)
	    	test_tweets.append((featureVector))
	    	print featureVector
	    	test_feature_vector = getSVMFeatureVector(test_tweets, featureList)
	    	k = 0
		p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),test_feature_vector, classifier)
		test_tweets.remove(featureVector)
		outTweet.writerow((p_labels))
		a.append(p_labels)	
		k = 0
		if(a[0][0] == 1.0):
          		fact.write("positive "+"\t"+t+"\n")
			sentiment = {"sentiment" : "positive"}
			docs[i].update(sentiment)
        	elif(a[0][0] == 2.0):
          		fact.write("neutral"+"\t"+t+"\n")
			sentiment = {"sentiment" : "neutral"}
                	docs[i].update(sentiment)

      		elif(a[0][0] == 0.0):
         		fact.write("negative"+"\t"+t+"\n")
			sentiment = {"sentiment" : "negative"}
                	docs[i].update(sentiment)
          	
		a.remove(p_labels)

       	 	i = i+1
k = 0;
db.update(docs)

for lm in doc2:
	fact1.write(lm+"\n ")

fact.close()
fact1.close()

