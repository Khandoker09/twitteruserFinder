
'''
Purpose: collect users info from twitter by search quary keywords.
Methods : use tweepy and api key from my delveloper accounts 
Author : Khandoker Tanjim Ahammad
published : 2022- 02- 15
Remakrs : still need to fix the rate limits 

'''
import tkinter as tk
import tweepy
import time
from tweepy import OAuthHandler
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag, pos_tag_sents
import re
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
import datetime
current_date = datetime.datetime.now()
# root window
root = tk.Tk()
root.geometry('500x200')
root.resizable(0,0)
root.title('Twitter Data GeneratorV-2.0')

def my_function():
    #twitter credentials
    consumer_key = "API KEY"
    consumer_secret = "API KEY"
    access_key = "API KEY"
    access_secret = "API KEY"
    # Pass your twitter credentials to tweepy via its OAuthHandler
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    api.wait_on_rate_limit = True
    api.wait_on_rate_limit_notify = True
    api = tweepy.API(auth, wait_on_rate_limit=True)
    id = my_entry.get()
    text_query = (id)#'managing editor'
    max_tweets = 1000
  
    # Creation of query method using parameters
    tweets = tweepy.Cursor(api.search_users,q=text_query ,count=5,include_entities=True).items(max_tweets)  #
    
    # Pulling information from tweets iterable object
    try:
    # Add or remove tweet information you want in the below list comprehension
        tweets_list = [[tweet.name,tweet.screen_name, tweet.id_str,tweet.location, tweet.url, tweet.description, tweet.verified, tweet.followers_count, tweet.friends_count, tweet.statuses_count, tweet.listed_count, tweet.created_at, tweet.profile_image_url_https, tweet.default_profile] for tweet in tweets]
    # Creation of dataframe from tweets_list
    except:
        tweets_list = [[tweet.name,tweet.screen_name, tweet.id_str,tweet.location, tweet.url, tweet.description, tweet.verified, tweet.followers_count, tweet.friends_count, tweet.statuses_count, tweet.listed_count, tweet.created_at, tweet.profile_image_url_https, tweet.default_profile] for tweet in tweets]
        time.sleep(10)
    # Did not include column names to simplify code 
    tweets_df = pd.DataFrame(tweets_list)
    tweets_df.columns = ['username','user_screenname','userid','userslocation','usersurl','usersdescription','userverified','followerscount','friendscount','statusescount','listedcount','createdat','profileimageurlhttps','defaultrofile']
    tweets_df[['firstname','lastname']] =   tweets_df['username'].loc[  tweets_df['username'].str.split().str.len() == 2].str.split(expand=True)
    tweets_df=tweets_df[['username','firstname','lastname','user_screenname','userid','userslocation','usersdescription','followerscount']]
    # use regex to figureout the company name  @([\w.-]+)\.
    tweets_df['employeecompany'] = tweets_df['usersdescription'].str.extract(r'@([\w.-]+)\.', expand=False) 
    tweets_df=tweets_df[['username','firstname','lastname','employeecompany','user_screenname','userid','userslocation','usersdescription','followerscount']]
    #tweets_df['POSTags'] = pos_tag_sents(tweets_df['usersdescription'].apply(word_tokenize).tolist())
    filename = str('twitter_search_list_')+str(current_date.year)+str('_')+str(current_date.month)+str('_')+str(current_date.day)
    print(tweets_df)
  
    tweets_df.to_csv(str(text_query+filename + '.csv'),index=False)
    
   

my_label = tk.Label(root, text = "Enter the twitter query ")
my_label.grid(row = 0, column = 0)
my_entry = tk.Entry(root)
my_entry.grid(row = 0, column = 1)

my_button = tk.Button(root, text = "Submit", command = my_function)
my_button.grid(row = 1, column = 1)

root.mainloop()
