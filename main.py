#!/usr/bin/python3.4

import twitter_interface as ti
import user_interact as ui

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

	
	(initial_state, worlds)=ui.load(database_path)	

	for (tweet_id,tweet_text) in ti.get_new_tweets():
		if world:
			exists=False
			for room in world: 	
				interaction=room.interact(tweet_text)	
				if interaction:
					exists=True
			if exists: ti.dm_tweet_to_admins(tweet_id)	
		else:
			ti.dm_tweet_to_admins(tweet_id, "empty world")
