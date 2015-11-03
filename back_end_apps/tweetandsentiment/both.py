#Author :Kalyan Pichumani and Saranya Nagarajan 
#Referance :http://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
#http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
#This program will extract tweets on query which is specified and predicts the sentiment of every tweet
#Run this program python both.py -s query
import goslate
import couchdb
import argparse
import re
import csv
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import svmutil
import nltk
from svmutil import *
import sys
import json
import TweetBase
import twitter
import tweepy

sID = None
mID = -1L
total =0

#multiple user accounts are being authenticated and added to a list 
class clientKeys:
	
	def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret, clientid):
		self.access_token = access_token
		self.access_token_secret = access_token_secret
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.clientid = clientid
		
	def OAuth(self):
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		client = tweepy.API(auth)
		return client

clients = []
details1 = clientKeys("137367359-xTFdQYSCcAJoPGlSyHuQAxP3ieLtGUiLN8FKiduI", "QSAYSrDVRFOckQfJ5qxp4vrkPXDSIzbQKHFCTOtDJXSKx", "nFhq44qf9GVoSp7DSfWtOYkI6", "YXXsC47XryCaG5690Wj1rpHjHu791QEGIN7jIwimetZWX9FDph", 1)
details1.handle = details1.OAuth()
clients.append(details1)
details2 = clientKeys("3161564544-U6YLon0E6N7ZvHtfvoeHRSdlCp4NbjHGd1acrBN", "FaaZcVA2847YNA2igjFjjKpQvIgVUCNlh8H3ZvP2ey0Ro", "WxOvbrNAzyjy7vszxJ6OLeyol", "1s7s2f4SeryTN374dGMvoSwtXM10JHOYRVEd6JcJirqFYK9BE9", 2)
details2.handle = details2.OAuth()
clients.append(details2)
details3 = clientKeys("128415623-tbIJqZujbYoYP4xsPleUWthHO7W6jnu5LscL6AAA", "wSmbC1oRINjcnAvmCzbOABn8lsJ6GOxtZONGe6o80uEtr", "OvFt3ix2aummG26HtS8sT1MzU", "71tH27a3HljrW1cEOuoFZRPfmnZFqxhf4UXLI13rhgHfUA8mQ0", 3)
details3.handle = details3.OAuth()
clients.append(details3)
details4 = clientKeys("2401399747-HGxObwgYtp2aFO6whX0GoQwNEn4E4yxK7mkHjEn", "miPNtaUNvGDct6oKWJKO9SNZYYdIAzMG2aHODnfgadwMM", "tsa7I86gihfEKCRfyQ8sM3ruc", "rgGJJPser76YhlljzVFvo2V5qUaoZnaGxxaC5CdyZBqsKgYEim", 4)
details4.handle = details4.OAuth()
clients.append(details4)
details5 = clientKeys("1345785727-4q81KjFTZc5oFu0eEi3uxpQxiIKQRv2qZKjpYQv", "LxHj4ymGyvBrtVhTdXO1iBcskFemj4IYn6w0s9BD6K2K5", "40pGYbUc8fZ5CkEsw4VTsyWqH", "TIxs2MMNuSJkwAmuGWAdCOamNKtrI7VaPJelrAkPhI4kpw3pqm", 5)
details5.handle = details5.OAuth()
clients.append(details5)
details6 = clientKeys("3522828433-xdClye90mkKqwSXGMwpIvnOZsvtx5XaecCbmnMR", "8D3jM1gsw0iTYKeJUvwGPqFkIbt2pweJWIDk2Gv5RZk1u", "oboRwqkiL05oePIWXpRL8WJUF", "IdGHjwmj3yS5U99Bb2rU1sGMBT2YKHMoIzJHvWopYb9Khxe7LQ", 6)
details6.handle = details6.OAuth()
clients.append(details6)


def cli_format():
	
	print "Consumer-key,consumer-secret,access-token,access-token-secret"

def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fStopList = open(stopWordListFileName, 'r')
    line = fStopList.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fStopList.readline()
    fStopList.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet,stopWords):
	featureVector = []
	alligator = 0
	effect = 0
	#split tweet into words
	words = tweet.split()
	for w in words:
		#replace two or more with two occurrences
		w = replaceTwoOrMore(w)
		#strip punctuation
		w = w.strip('\'"?,.')
		#check if the word stats with an alphabet
		val = re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', w)
		pattern = re.compile(r'/[ \t]+/')
		result = pattern.match(w)
		#ignore if it is a stop word
		#print 
		if(w in stopWords or val is None):
			continue
		else:
		    if(result != None):
			pattern = re.compile(r'/[ \t]+/')
                	result = pattern.match(w)
			featureVector.append(result.lower())
			print result
		    else:	
			featureVector.append(w.lower())
	return featureVector
#end

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r'(.)\1{1,}', re.DOTALL)
    return pattern.sub(r'\1\1', s)
#end

#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    #tweet_words = tweet
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
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

        tweet_words = t[0]
        tweet_opinion = t[1]
        #Fill the map
        for word in tweet_words:
            #process the word (remove repetitions and punctuations)
            word = replaceTwoOrMore(word)
            word = word.strip('\'"?,.')
            #set map[word] to 1 if word exists
            if word in map:
                map[word] = 1
        #end for loop
        values = map.values()
        feature_vector.append(values)
        if(tweet_opinion == 'positive'):
            label = 0
        elif(tweet_opinion == 'negative'):
            label = 1
        elif(tweet_opinion == 'neutral'):
            label = 2
        labels.append(label)
		
    
	#return the list of feature_vector and labels
	#print {'feature_vector' : feature_vector, 'labels': labels}
    return {'feature_vector' : feature_vector, 'labels': labels}
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

        tweet_words = t
        #tweet_opinion = t[1]
        #Fill the map
        for word in tweet_words:
            #process the word (remove repetitions and punctuations)
            word = replaceTwoOrMore(word)
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

#removes the stopwords using the list available
stopWords = []	
st = open('StopWords.txt', 'r')
stopWords = getStopWordList('StopWords.txt')
counter = 0;
inpTweets = csv.reader(open('mycsv.csv',"rU"), dialect='excel-tab') #delimiter =',', quotechar = '|')
outTweet = csv.writer(open('TestResultSVM.csv',"wb"), dialect='excel-tab')
featureList = []
tweets = []
#retrieves the featureVector
for row in inpTweets:
	sentiment = row[0]
	tweet = row[1]
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
#fts.write(result)
# Remove featureList duplicates
featureList = list(set(featureList))

fts.close()
fact = open("test.txt","w")
# Test the classifier
fact1 = open("test1.csv","w")
doc2=[]
test_tweets =[]
test_tweets1 = []
i = 0
a = []

#saves the tweet in database
def save_tweet(db,tweet):
		
		gs=goslate.Goslate()
		json_str = json.loads(json.dumps(tweet._json))	
		json_str['_id'] = json_str['id_str']
		#translate the tweet to English before saving
		if (json_str["lang"] != 'en'):
			text = gs.translate(json_str["text"],'en')
			translated_text = {"translated_text" : text}
			json_str.update(translated_text)
			print translated_text
			t=text.encode("utf-8")
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
			if(a[0][0] == 1.0):
          			fact.write("positive "+"\t"+t+"\n")
				sentiment = {"sentiment" : "positive"}
				json_str.update(sentiment)

  		        elif(a[0][0] == 2.0):
          			fact.write("neutral"+"\t"+t+"\n")
				sentiment = {"sentiment" : "neutral"}
                    		json_str.update(sentiment)

			elif(a[0][0] == 0.0):
        	 		fact.write("negative"+"\t"+t+"\n")
				sentiment = {"sentiment" : "negative"}
	                	json_str.update(sentiment)

   
			a.remove(p_labels)

		else:
			translated_text = {"translated_text" : json_str["text"]}
            		json_str.update(translated_text)
			print translated_text
			t=json_str["text"].encode("utf-8")
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
			if(a[0][0] == 1.0):
          			fact.write("positive "+"\t"+t+"\n")
         			print "1111111111111111"
				sentiment = {"sentiment" : "positive"}
				json_str.update(sentiment)

  		    	elif(a[0][0] == 2.0):
          			fact.write("neutral"+"\t"+t+"\n")
				print "@2222222222222222222"
				sentiment = {"sentiment" : "neutral"}
                    		json_str.update(sentiment)

	      		elif(a[0][0] == 0.0):
        	 		fact.write("negative"+"\t"+t+"\n")
				print "4444444444444444"
				sentiment = {"sentiment" : "negative"}
	                	json_str.update(sentiment)

   
			a.remove(p_labels)

		db.save(json_str)
		return 1
	        


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--query", required=True, help="Query for which value to be retrieved")
args = vars(ap.parse_args())

totalTweets = 1000000
#maximum per page
perPage = 100
value = args ['query']

server = couchdb.Server()

db = server['tweets']
#db = server['poverty']
for each in clients:
		client = each.handle
		try:
			g = client.rate_limit_status()
			r = g[u'resources'][u'search'][u'/search/tweets'][u'remaining']
		except Exception:
			r = 0
		if r > 0:
			print each.clientid, " started"
			break
while total < totalTweets:

 try:
			#tweets =tweepy.Cursor(client.search, q = 'poverty').items()
			if mID <= 0:
				if not sID:
					tweets =tweepy.Cursor(client.search, q = value,count=perPage).items()

				else:
					tweets =tweepy.Cursor(client.search, q = value, since_id=sID,count=perPage).items()

					#new_tweets = client.search(q=searchQuery, count=perPage, since_id=sID)
			else:
				if not sID:
					tweets =tweepy.Cursor(client.search, q = value, mID=str(mID - 1),count=perPage).items() 
					#new_tweets = client.search(q=searchQuery, count=perPage, mID=str(mID - 1))
				else:
					tweets =tweepy.Cursor(client.search, q = value, mID=str(mID - 1), since_id=sID,count=perPage).items()

				#	new_tweets = client.search(q=searchQuery, count=perPage, mID=str(mID - 1), since_id=sID)
			if not tweets:
               			 print("No more tweets found")
               			 break
			counter = 0
			total = total+1
			for tweet in tweets:
    			 try:	
	    			counter += save_tweet(db,tweet)

	        		print counter
		
    			 except Exception:	
				pass
 except tweepy.TweepError as e:
			print("some error : " + str(e))
			print "Switching user"
			for each in clients:
				client = each.handle
				try:
					g = client.rate_limit_status()
					r = g[u'resources'][u'search'][u'/search/tweets'][u'remaining']
				except Exception:
					r = 0
				if r > 0:
					print each.clientid, " started"
					break
for lm in doc2:
	fact1.write(lm+"\n ")

fact.close()
fact1.close()



