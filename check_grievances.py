#!/usr/bin/env python3

import tweepy
import urllib3
from settings import *
from urllib.parse import quote

#This will check for DMs sent to the bot, post them to Google form
#send a response and delete the DM


try:
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	dms = api.direct_messages(full_text=True)
	http = urllib3.PoolManager()

	for m in dms:
		if len(m.text) > 280:
			mres = api.send_direct_message(m.sender.screen_name, text="Oops. Your grievance is longer than 280 characters, please try again.")
			print("LONG "+m.text)
			r = http.request('GET',GFORM_URL+quote("LONG "+m.text))
		else:
			mres = api.send_direct_message(m.sender.screen_name, text="Thanks, your grievance has been queued for approval. More details here: http://lisgrievances.com/about.html")
			print(m.text)
			#Grievances are tabulated annoymously in a Google Form where they are eventually posted
			#This part of the process will be automated in future version
			r = http.request('GET',GFORM_URL+quote(m.text))

		#Destroy the message received and the response to it
		api.destroy_direct_message(m.id)
		api.destroy_direct_message(mres.id)
	print("Done Checking")

except:
	print("Could not connect to Twitter to check")


# Delete any lingering DMs by borking them
try:
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	dms = api.direct_messages()
	# The nuclear option, will delete all DM's to the bot.
	for m in dms:
		api.destroy_direct_message(m.id)
	print("Done Borking")
except:
	print("Could not connect to twitter to bork")

