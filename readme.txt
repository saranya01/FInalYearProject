CouchDB URL
- 115.146.94.14:5984/_utils/
- 115.146.95.154:5984/_utils/
Web URL
- http://115.146.95.154:98/aja/sentiment-analysis.html - to visualize the data analysis
- http://115.146.95.154:98/aja/adb.html - to view the organization and their followers.

Procedure to run the code
  Tweets Harvesting and Sentiments
CouchDB has to be established and the database name in the code has to be changed to the corresponding database name.
Five different codes have been presented for this part of analysis
- First part is to just extract the tweets from twitter and store it in CouchDB (harvest.py). To run this code, "python harvest.py -s 'query name/hashtag' " command has to be used.
- Second part is timeline harvesting. To run this code, "python time.py -s 'screenname' " command has to be used.
- Third part of code is to extract tweets from Topsy and store it in CouchDB. To run this code, "python topsy.py -s 'query name/hashtag' " command has to be used.
-Fourth part of code is to extract tweet text from CouchDB, predicts the sentiment and stores the sentiment as new field on every document in the couchDB. To run this code, "python sentiment.py" command has to be used. This program is provided in a different folder "sentiment" to make sure all the add-on files are correctly provided make the program run.
- Last part of code is to extract tweet text from Twitter directly, predicts the sentiment and stores everything together in the couchDB. To run this code, "python Both.py -s 'queryname/hashtag ' " command has to be used. For convenience this program is provided in a different folder "tweetSentiment" to make sure all the add-on files are correctly provided make the program run.
Harvesting Organization Data
- This part has one code which extracts all the details of organization and maps an edge between all the organization and stores the data in CouchDB. 
-To run this code, "python processGraph.py -s 'screenname ' -d '1/2/3' " command has to be used. 
For convenience this program is provided in a different folder "Processgraph" to make sure all the add-on files are correctly provided make the program run. 
And "-d" in the command signifies the depth level up to which the data need to be retrieved, accordingly the value can be given either as '1' or '2' or '3'.
