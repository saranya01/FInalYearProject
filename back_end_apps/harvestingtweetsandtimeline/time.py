#Author :Kalyan Pichumani and Saranya Nagarajan 
#Referance :http://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
#This program will extract tweets on on users timeline
#Run this program python time.py -s screenname

import argparse
import twitter
import sys
import couchdb
import json
import TweetBase
import goslate

def save_tweet(db,tweet):
		gs=goslate.Goslate()
		
		#Translating the tweet to english
		tweet['_id'] = tweet ['id_str']
			#creates a new column in database and stores it as an attribute
		if (tweet["lang"] != 'en'):
                        text = gs.translate(tweet["text"],'en')
                        translated_text = {"translated_text" : text}
                        tweet.update(translated_text)
                        print translated_text
                else:
                        translated_text = {"translated_text" : tweet["text"]}
                        tweet.update(translated_text)
                        print translated_text

                db.save(tweet)
                return 1


def login():

   # This mode of authentication is the new preferred way
    CONSUMER_KEY = 'nFhq44qf9GVoSp7DSfWtOYkI6'
    CONSUMER_SECRET = 'YXXsC47XryCaG5690Wj1rpHjHu791QEGIN7jIwimetZWX9FDph'
    OAUTH_TOKEN = '137367359-xTFdQYSCcAJoPGlSyHuQAxP3ieLtGUiLN8FKiduI'
    OAUTH_TOKEN_SECRET = 'QSAYSrDVRFOckQfJ5qxp4vrkPXDSIzbQKHFCTOtDJXSKx'

    # Creating the authentification
    auth = twitter.oauth.OAuth( OAUTH_TOKEN,
                                OAUTH_TOKEN_SECRET,
                                CONSUMER_KEY,
                                CONSUMER_SECRET )
    # Twitter instance
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
#argument to be passed 
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
args = vars(ap.parse_args())
seed = args['screen_name']

twitter_api = login()
server = couchdb.Server()
db = server['time']
list = []
#retrieves first 200 tweets fom the timeline
totalTweets = twitter_api.statuses.user_timeline(screen_name=seed,count = 200)
list.extend(totalTweets)
maximum = list[-1]['id'] - 1
total = 0
count = 0
while len(totalTweets) > 0:
	totalTweets = twitter_api.statuses.user_timeline(screen_name=seed,count = 200,max_id=maximum)
	count += len(totalTweets)
        # save most recent totalTweets
        list.extend(totalTweets)

           
	maximum = list[-1]['id'] - 1

for tweet in list:
    try:
        total += save_tweet(db,tweet)
        print total
	
    except Exception:
        pass
