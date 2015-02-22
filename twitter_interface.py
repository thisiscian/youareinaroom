#!/usr/bin/env python3
# Connect to the Twitter API please

import tweepy
import time

consumer = open("consumer.txt", "r").read().splitlines()
access = open("access.txt", "r").read().splitlines()

consumer_key = consumer[0]
consumer_secret = consumer[1]

access_token = access[0]
access_token_secret = access[1]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#https://github.com/tweepy/tweepy/issues/554
user = api.me()

def dm_tweet_to_admins(user, tweet_id, error = "Help me with this tweet!"):
    admins = open("admins.txt", "r")
    
    for line in admins:
        api.send_direct_message(user = line, text = error + " https://twitter.com/" + str(user) + "/status/" + str(tweet_id))

def get_mentions():
    latest_id = None
    
    while(True):
        try:
            tweets = api.search(to = user.screen_name, since_id = latest_id)
            latest_id = tweets[0].id

            for tweet in tweets:
                print("@" + tweet.user.screen_name + ":")
                print(tweet.text + "\n")
        
            time.sleep(0)
            print(tweets[0].id)

        except KeyboardInterrupt:
            return -1
        except:
            continue

if __name__ == "__main__":

    get_mentions()

