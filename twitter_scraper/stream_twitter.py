
# coding: utf-8

# # What key words do you want to look for in twitter

# In[5]:

# key_words_list = ['San Francisco']
key_words_list = []


# # import tweepy tools, dont forget to "pip install tweepy" in your shell

# In[11]:

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import TwitterAuth
import sys

#Very simple (non-production) Twitter stream example
#1. Download / install python and tweepy (pip install tweepy)
#2. Fill in information in auth.py
#3. Run as: python streaming_simple.py
#4. It will keep running until the user presses ctrl+c to exit
#All output stored to output.json (one tweet  per line)
#Text of tweets also printed as recieved (see note about not doing this in production (final) code

results_path = './results/'

if sys.argv[1] == '-f':
    out_file = results_path+'output.json'
else:
    out_file = sys.argv[1]

class StdOutListener(StreamListener):

    #This function gets called every time a new tweet is received on the stream
    def on_data(self, data):
        #Just write data to one line in the file
        fhOut.write(data)

        #Convert the data to a json object (shouldn't do this in production; might slow down and miss tweets)
        j=json.loads(data)

        #See Twitter reference for what fields are included -- https://dev.twitter.com/docs/platform-objects/tweets
        text=j["text"] #The text of the tweet
        print(text) #Print it out

    def on_error(self, status):
        print("ERROR")
        print(status)

print out_file


# # run the script that streams the twitter data and saves it to the file output.json

# In[23]:


try:
    #Create a file to store output. "a" means append (add on to previous file)
    fhOut = open(out_file,"a")

    #Create the listener
    l = StdOutListener()
    auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
    auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

    #Connect to the Twitter stream
    stream = Stream(auth, l)

    #Terms to track
    #stream.filter(track = key_words_list) #track=["oxford","london","wolverhampton"])

    #Alternatively, location box  for geotagged tweets
    stream.filter(locations=[-122.75,36.8,-121.75,37.8])

except (RuntimeError, TypeError, NameError, KeyboardInterrupt):
    #User pressed ctrl+c -- get ready to exit the program
    #print e
    #Close the 
    fhOut.close()




# In[24]:

fhOut.close()


# In[ ]:



