#Author :Kalyan Pichumani and Saranya Nagarajan 
#Referance :http://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
#This program will extract tweets on query which is specified
#Run this program python harvest2.py -s query
import sys
import couchdb
import json
import TweetBase
import goslate
import twitter
import tweepy
import argparse
#multiple user accounts are being authenticated and added to a list 
sID = None
mID = -1L
total =0

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

def save_tweet(db,tweet):
		
		gs=goslate.Goslate()
		json_str = json.loads(json.dumps(tweet._json))	
		json_str['_id'] = json_str['id_str']
		#stores the translated text as a new attribute in database
		if (json_str["lang"] != 'en'):
			text = gs.translate(json_str["text"],'en')
			translated_text = {"translated_text" : text}
			json_str.update(translated_text)
			print translated_text
		else:
			translated_text = {"translated_text" : json_str["text"]}
	                json_str.update(translated_text)
			print translated_text

		db.save(json_str)
		return 1
	        
#Argument to be passed
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--query", required=True, help="Query for which value to be retrieved")
args = vars(ap.parse_args())

maxTweets = 1000000
perPage = 100
value = args ['query']

server = couchdb.Server()
#CouchDB database name
db = server['tweets']
for each in clients:
		client = each.handle
		try:
		#As twitter allows an user to extract only 200 friends at max per call after which rate limit exception occurs ,to extract more user ratelimit status is used 
				
			g = client.rate_limit_status()
			remaining = g[u'resources'][u'search'][u'/search/tweets'][u'remaining']
		except Exception:
			remaining = 0
		if remaining > 0:
			break
while total < maxTweets:

 try:
			if mID <= 0:
				if not sID:
					tweets =tweepy.Cursor(client.search, q = value,count=perPage).items()

				else:
					tweets =tweepy.Cursor(client.search, q = value, since_id=sID,count=perPage).items()

					
			else:
				if not sID:
					tweets =tweepy.Cursor(client.search, q = value, mID=str(mID - 1),count=perPage).items() 
				else:
					tweets =tweepy.Cursor(client.search, q = value, mID=str(mID - 1), since_id=sID,count=perPage).items()

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
					remaining = g[u'resources'][u'search'][u'/search/tweets'][u'remaining']
				except Exception:
					remaining = 0
				if remaining > 0:
					print each.clientid, " started"
					break

