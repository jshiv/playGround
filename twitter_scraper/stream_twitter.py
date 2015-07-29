
# coding: utf-8

# # What key words do you want to look for in twitter

# # import tweepy tools, dont forget to "pip install tweepy" in your shell

# In[5]:

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import TwitterAuth
import sys

import time
import os

#Very simple (non-production) Twitter stream example
#1. Download / install python and tweepy (pip install tweepy)
#2. Fill in information in auth.py
#3. Run as: python streaming_simple.py
#4. It will keep running until the user presses ctrl+c to exit
#All output stored to output.json (one tweet  per line)
#Text of tweets also printed as recieved (see note about not doing this in production (final) code

# results_path = './results/'

# if sys.argv[1] == '-f':
#     out_file = results_path+'output.json'
# else:
#     out_file = sys.argv[1]

class StdOutListener(StreamListener):

    def __init__(self,file_handle, production = True, stop = 1000):
        self.file_handle = file_handle
        self.production = production
        self.counter = 0
        self.stop = stop
    #This function gets called every time a new tweet is received on the stream
    def on_data(self, data):
        #Just write data to one line in the file
        self.file_handle.write(data)
        self.counter += 1

        if self.production == False:
            #Convert the data to a json object (shouldn't do this in production; might slow down and miss tweets)
            j=json.loads(data)

            #See Twitter reference for what fields are included -- https://dev.twitter.com/docs/platform-objects/tweets
            text=j["text"] #The text of the tweet
            print(text) #Print it out
        if self.counter >= self.stop:
            broken

    def on_error(self, status):
        print("ERROR")
        print(status)



# # run the script that streams the twitter data and saves it to the file output.json

# In[7]:


if sys.argv[1] == '-f':
    production = False
    stop = 4
else:
    production = True
    stop = 1000
    
print 'production is ',production,' stop in: ',stop


# In[8]:


try:
    os.mkdir('./results')
except:
    pass


# In[13]:

def write_stream(out_file, production = False, stop = 1000, locations = [-122.75,36.8,-121.75,37.8]):
    try:
        #Create a file to store output. "a" means append (add on to previous file)
        fhOut = open(out_file,"a")

        #Create the listener
        l = StdOutListener(fhOut, production = production, stop = stop)
        auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
        auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

        #Connect to the Twitter stream
        stream = Stream(auth, l, timeout=60)

        #Terms to track
        #stream.filter(track = key_words_list) #track=["oxford","london","wolverhampton"])

        #Alternatively, location box  for geotagged tweets
        stream.filter(locations=locations)#[-122.3145,37.3643,-122.2037,37.4855])

        #stream.filter(locations=[-122.75,36.8,-121.75,37.8])
        #$$c(W 122°31'45"--W 122°20'37"/N 37°48'55"--N 37°36'43")

    except (RuntimeError, TypeError, NameError, KeyboardInterrupt):
        #User pressed ctrl+c -- get ready to exit the program
        #Close the 
        fhOut.close()


if __name__=='__main__':
#     while True:
    if production:
        while True:
            try:
                write_stream('./results/tweets'+str(int(time.time()))+'.json', 
                             production = production, 
                             stop = stop, 
                             locations = [-122.75,36.66,-122.35,37.82])

            except:
                continue
    else:
        try:
            write_stream('./results/tweets'+str(int(time.time()))+'.json', 
                         production = production, 
                         stop = stop, 
                         locations = [-122.75,36.66,-122.35,37.82])

        except Exception as e:
            print e#continue

