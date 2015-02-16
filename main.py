import twitter_interface as ti
import user_interact as ui

world=[]

if __name__=="__main__":
	for (tweet_id,tweet_text) in ti.get_new_tweets():
		if world:
			exists=False
			for room in world: 	
				interaction=room.interact(tweet_text)	
				if interaction:
					exists=True
			if exists: ti.dm_tweet_to_admins(tweet_id)	
		else:
			ti.dm_tweet_to_admins(tweet_id, "empty world ")
