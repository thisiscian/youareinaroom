#!/usr/bin/python3.4

import twitter_interface as ti
from random import choice

if __name__=="__main__":
	import sys
	import os
	if len(sys.argv) < 2: 
		print("\x1b[31;1mError\x1b[0m: you should add a database, you fool")
		exit(1)
	database_path=sys.argv[1]
	if not os.path.isfile(database_path):
		print("\x1b[31;1mError\x1b[0m: could not find supplied database \""+database_path+"\"")
		exit(1)
	database=Database(database_path)
			
	while(True):
		for (tweet_id,tweet_text) in ti.get_new_tweets():
			results=database.find_command(tweet_text)
			if results is None:
				if database.is_user(user):
					ti.dm_tweet_to_admins(tweet_id)	
				else:	
					continue	
			(response,change)=choice(results)
			new_state=database.change_state(user,change)	
			if new_state == '0':
				database.add_user(user)
			else:
				database.update_state(user,new_state)
			tweet(response)
