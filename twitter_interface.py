#!/usr/bin/env python3
# Connect to the Twitter API please

import tweepy

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
user = api.get_user(screen_name = "youareinaroom")

def dm_tweet_to_admins(user, tweet_id, error = "Help me with this tweet!"):
    admins = open("admins.txt", "r")
    
    for line in admins:
        api.send_direct_message(user = line, text = error + " https://twitter.com/" + str(user) + "/status/" + str(tweet_id))

if __name__ == "__main__":

    dm_tweet_to_admins("octopotus", "567364462207041536")    



