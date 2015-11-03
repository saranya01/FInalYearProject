#Author :Kalyan Pichumani and Saranya Nagarajan 
#Referance : http://mark-kay.net/2014/08/15/network-graph-of-twitter-followers/
#This program will extract followers of a twitter user who's screen name has been specified
#Run this program python processGraph.py -s screenname -d 1
import time
import os
import geocoder
import sys
import json
import argparse
import tweepy
import glob
import csv
import couchdb
import requests
import geopy
from collections import defaultdict
from uuid import uuid4
from geopy.geocoders import Nominatim
geolocator = Nominatim() 
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

#Takes in the directory name which has to be created and checks whether the directory is present
FOLLOWING_DIR = 'following'
MAX_FRIENDS = 300
FRIENDS_OF_FRIENDS_LIMIT = 500
if not os.path.exists(FOLLOWING_DIR):
    os.makedir(FOLLOWING_DIR)
client = clients[1].handle
a=1
enc = lambda x: x.encode('ascii', errors='ignore')
#Account details of a twitter user
CONSUMER_KEY = 'nFhq44qf9GVoSp7DSfWtOYkI6'
CONSUMER_SECRET = 'YXXsC47XryCaG5690Wj1rpHjHu791QEGIN7jIwimetZWX9FDph'
ACCESS_TOKEN = '137367359-xTFdQYSCcAJoPGlSyHuQAxP3ieLtGUiLN8FKiduI'
ACCESS_TOKEN_SECRET = 'QSAYSrDVRFOckQfJ5qxp4vrkPXDSIzbQKHFCTOtDJXSKx'

def get_follower_ids(centre,client, max_depth=1, current_depth=0, taboo_list=[]):
 if(max_depth == 1): 	
    client = client	
    if current_depth == max_depth:
        print 'out of depth'
        return taboo_list
    if centre in taboo_list:
        print 'Already been here.'
        return taboo_list
    else:
        taboo_list.append(centre)
 
    try:
        userfname = os.path.join('twitter-users', str(centre) + '.json')
        if not os.path.exists(userfname):
            print 'Retrieving user details for twitter id %s' % str(centre)
            while True:
                try:
					#Function in tweepy which returns all the details of an user
                    user = client.get_user(centre)
					#Geo location converter, takes in the location as input and produces the geo code as output.
	  	    l = geolocator.geocode(user.location)
                    location_latlng=l.latitude,l.longitude
                    print location_latlng
					#stores all the details in a dictionary
		    print user.id	
                    d = {'name': user.name,
                         'screen_name': user.screen_name,
                         'id': user.id,
                         'friends_count': user.friends_count,
                         'followers_count': user.followers_count,
                         'followers_ids': user.followers_ids(),
						 'location' : user.location,
							'URL' : user.url,'lat-long' : location_latlng}
 
                    with open(userfname, 'w') as outf:
                        outf.write(json.dumps(d, indent=1))
			print outf
                    user = d
                    break
                except tweepy.TweepError, error:
                    print type(error)
 
                    if str(error) == 'Not authorized.':
                        print 'Can''t access user data - not authorized.'
                        return taboo_list
 
                    if str(error) == 'User has been suspended.':
                        print 'User suspended.'
                        return taboo_list
 
                    errorObj = error[0][0]
                    print errorObj
 
                    if errorObj['message'] == 'Rate limit exceeded':
                        print 'Rate limited. Sleeping for 15 minutes.'
                        continue
                    return taboo_list
        else:
            user = json.loads(file(userfname).read())
 
        screen_name = enc(user['screen_name'])
        fname = os.path.join(FOLLOWING_DIR, screen_name + '.csv')
        friendids = []
        # only retrieve friends of TED... screen names
        if not os.path.exists(fname):
                print 'No cached data for screen name "%s"' % screen_name
                with open(fname, 'w') as outf:
                    params = (enc(user['name']), screen_name)
                    print 'Retrieving friends for user "%s" (%s)' % params
					#Tweepy function which takes in Id of the primary user and Id of the friends and returns all the details about the friends
                    c = tweepy.Cursor(client.friends, id=user['id']).items()

                    friend_count = 0
                    while True:
                        try:
                            friend = c.next()
                            friendids.append(friend.id)
                            params = (friend.id, enc(friend.screen_name), enc(friend.name),enc(friend.location),friend.url)
                            outf.write('%s\t%s\t%s\t%s\t%s\t\n' % params)
                            friend_count += 1
                            if friend_count >= MAX_FRIENDS:
                                print 'Reached max no. of friends for "%s".' % friend.screen_name
                                break
                        except tweepy.TweepError:
			    for eachClient in clients:
				client = eachClient.handle
				try:
				#As twitter allows an user to extract only 200 friends at max per call after which rate limit exception occurs ,to extract more user ratelimit status is used 
					g = client.rate_limit_status()
					#check whether the accounts maximum friends is exceeded, if so it switches to new user 
					remaining = g[u'resources'][u'friends'][u'/friends/list'][u'remaining']
				except Exception:
					remaining = 0
                                if remaining > 0:
                                       print eachClient.clientid, " started"
				       c = tweepy.Cursor(client.friends, id=user['id']).items()

                                       break
                        except StopIteration:
                            break
        print 'Found %d friends for %s' % (len(friendids), screen_name)
        cd = current_depth
        if cd+1 < max_depth:
                for fid in friendids[:FRIENDS_OF_FRIENDS_LIMIT]:
                    taboo_list = get_follower_ids(fid,client, max_depth=max_depth,
                        current_depth=cd+1, taboo_list=taboo_list )
 
                if cd+1 < max_depth and len(friendids) > FRIENDS_OF_FRIENDS_LIMIT:
                    print 'Not all friends retrieved for %s.' % screen_name
    except Exception, error:
            print 'Error retrieving followers for user id: ', centre
            print error
            return taboo_list
 else :
	print "error"
#Argument for the user to pass (screen name and depth)	
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
ap.add_argument("-d", "--depth", required=True, type=int, help="How far to follow user network")
args = vars(ap.parse_args())
twitter_screenname = args['screen_name']
depth = int(args['depth'])
if __name__ == '__main__':
    if depth < 1 or depth > 3:
        print 'Depth value %d is not valid. Valid range is 1-3.' % depth
        sys.exit('Invalid depth argument.')
 
    print 'Max Depth: %d' % depth
    matches = client.lookup_users(screen_names=[twitter_screenname])
    #print matches	
    if len(matches) == 1:
        print get_follower_ids(matches[0].id,client, max_depth=depth)
    else:
        print 'Sorry, could not find twitter user with screen name: %s' % twitter_screenname
################################################################################################################################
#Processes the collected details and creates nodes and edges to form a graph

users = defaultdict(lambda: { 'followers': 0 })
for f in glob.glob('twitter-users/*.json'):
    data = json.load(file(f))
    screen_name = data['screen_name']
    print  screen_name
    users[screen_name] = { 'followers': data['followers_count'] }
#User name as inuput	
SEED = twitter_screenname
server = couchdb.Server()
#CouchDB database name
db = server ['org']  
def process_follower_list(screen_name, edges=[], depth=0, max_depth=2):
#fetches data from 'following' directory 
    path = "/home/ubuntu/following"
    f = os.path.join(path, screen_name + '.csv')
    print f
    if not os.path.exists(f):
	 return edges
    followers = [line.strip().split('\t') for line in file(f)]
    #splits the entire line into tokens and stores all the values in different fields 
    for follower_data in followers:
        if len(follower_data) < 2:
            continue
        print "5"
	url =  follower_data[4]
        screen_name_2 = follower_data[1]
        try:
		if(follower_data[3] ):
			location = follower_data[3]
		else:
			location = "null"
	except IndexError:
		pass
        weight = users[screen_name]['followers']
	try:
	 if (location.startswith("T:") or location =="null"):
		location_latlng= location
	 else:
	 #geolocation converter
		l = geolocator.geocode(location)
		location_latlng=l.latitude,l.longitude
		print location_latlng
	except AttributeError :
		pass
	except geopy.exc.GeocoderTimedOut:
                            print 'Rate limited. Sleeping for 20 seconds.'
                            time.sleep(20)
                            continue
	except UnboundLocalError:
		pass
	try: 
   	 edges.append([screen_name, screen_name_2, weight,location,location_latlng,url])
 
         if depth+1 < max_depth:
            process_follower_list(screen_name_2, edges, depth+1, max_depth)
	    print "1" 
	except UnboundLocalError:
		pass 
    return edges
edges = process_follower_list(SEED, max_depth=3)
print "2"+ SEED
with open('twitter_network.csv', 'w') as outf:
    edge_exists = {}
    for edge in edges:
        key = ','.join([str(x) for x in edge])
        if not(key in edge_exists):
		#writes the data in this format in a CSV file
		outf.write('%s,%s,%d,%s,%s,%s\n' % (edge[0], edge[1], edge[2],edge[3],edge[4],edge[5]))

    		edge_exists[key] = True
csvfile = open('twitter_network.csv', 'r')
jsonfile = open('twitter-network.json', 'w')
fieldnames = ("name","followers","id","location","location_latlng","url")
data = []
i= 0
followers =[]
location=[]
latlng=[]
name = []
id_number = []
url=[]
for edge in edges:
        name.append(edge[0])
	id_number.append(edge[2])		
        break

for edge in edges:
        followers.append(edge[1])
        location.append(edge[3])
        latlng.append(edge[4])
	url.append(edge[5])

i=0
#data is converted to json and stored
data.append({'name' :name, 'id_number':id_number,'followers':followers,'location':location,'location_latlng':latlng ,'url':url})
i
print data
json.dump(data,jsonfile)
print data

