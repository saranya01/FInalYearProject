#Author :Kalyan Pichumani and Saranya Nagarajan 
#Referance :http://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
#https://github.com/dchud/toppsyy/blob/master/toppsyy.py
#This program will extract tweets on query which is specified
#Run this program python topsy.py -s query
import requests
import couchdb
import json 
import tweepy
import time
import sys
import argparse
from datetime import datetime

number = 1
#provides authentication
api_key = "09C43A9B270A470B8EB8F2946A9369F3"
last_offset = 0
mintime = 1438399845
maxtime = 1442374213
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
#Argument to be passed
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--query", required=True, help="Query for which value to be retrieved")
args = vars(ap.parse_args())

#query to be retriveed
location = args ['query']
tweet_textsStored = 0
server = couchdb.Server()
try:
	db = server.create('topsytweet_data_datechanged')
except Exception:
	db = server['topsytweet_data_datechanged']
try:
	for every in clients:
		client = every.handle
		try:
			g = client.rate_limit_status()
			left = g[u'resources'][u'statuses'][u'/statuses/show/:id'][u'remaining']
		except Exception:
			left = 0
		finally:	
			if left > 0:
				print every.clientid, " changed"
				break
	while True:
		print number
		try:
			request = requests.get("http://otter.topsy.com/search.json?q=%s&type=tweet&pernumber=1000&number=%s&mintime=%s&maxtime=%s&offset=%s&apikey=%s" % ("poverty%20", number, mintime, maxtime, last_offset, api_key))
	 		tweet_text = request.content
			#Converting the tweet to json
			tweet_data = json.loads(tweet_text)
			last_offset = tweet_data['response']['last_offset']
			for node in tweet_data['response']['list']:
				remaining = remaining + 1
				edge = node['trackback_permaedge']
				tweet_textId = edge[-18:]
				print tweet_textId
				date = node['trackback_date']
				node['tweet_text_date'] = str(datetime.fromtimestamp(float(date)))
				try:
					#Saving the tweet
					print "saving"
					db[node['content']] = node
					tweet_textsStored = tweet_textsStored + 1
					print "tweet_text stored"
				except couchdb.http.ResourceConflict:
					pass
			number = number + 1
			if number == 11:
				number = 1
				mintime = maxtime
				maxtime = maxtime + 600
				if maxtime > 1426377600:
					sys.exit()
		except Exception as e:
			pass
			
except KeyboardInterrupt:
	print "error"
