from flask import Flask, render_template, flash, Markup, json
#import urllib
#import webapp2
import os

from apiclient.discovery import build
#from google.appengine.ext import ext

import httplib2
import sys
import itertools
import logging
import logging.config
import time
import MySQLdb
	
#from googleapiclient.discovery import build_from_document
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.file import Storage
# from oauth2client.tools import argparser, run_flow
#from apiclient.errors import HttpError

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

global channel_id
global channel_Id
global user

#video_list_uploads = ['Daniel','George']

channel_list = ['UCgJA3nqJEUZBkZivasUSdJg']

@app.route('/')
def hello():
	video_list_uploads = []
	CLIENT_SECRETS_FILE = "client_secrets.json"
    
	YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"
	
#	return render_template('index.html', title = "Princess Elsa" , numbers = video_list_uploads)
	
# 	storage = Storage("static/main.py-oauth2.json")
# 	credentials = storage.get()
# 	
# 	logging.debug(storage)
# 	logging.debug(credentials)
	
#	return render_template('index.html', title = "Princess Elsa" , numbers = video_list_uploads)
	
# 	json_data = open("static/youtube-v3-discoverydocument.json")
# 	doc = json.load(json_data)
	
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey="AIzaSyBRgM5ARXMih_F9HviEUFYDpnkEmA4FPCs") 
	#http=credentials.authorize(httplib2.Http()))
   	
	for channelId in channel_list:

		channels_response = youtube.channels().list(id=channelId, part="contentDetails").execute()
	
		for channel in channels_response["items"]:
	
			try:
				uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["likes"]
			except KeyError:
				pass

			try:
				playlistitems_list_request = youtube.playlistItems().list(playlistId=uploads_list_id, part="snippet", maxResults=50)
			except NameError:
				pass
		
			try:
				while playlistitems_list_request:
					try:
						playlistitems_list_response = playlistitems_list_request.execute()
					except HttpError:
						pass
						# Print information about each video.
					for playlist_item in playlistitems_list_response["items"]:
					#title = playlist_item["snippet"]["title"]
						video_id = playlist_item["snippet"]["resourceId"]["videoId"]
						video_list_uploads.append([video_id])
					try:
						playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
					except HttpError:
						pass
			except NameError:
				pass
				
				
	env = os.getenv('SERVER_SOFTWARE')
	if (env and env.startswith('Google App Engine/')):
  	# Connecting from App Engine
  		db = MySQLdb.connect(
    	unix_socket='/cloudsql/peppy-linker-102423:daniel-george',
    	user='root',
    	db='sheepdog')
	else:
  	# You may also assign an IP Address from the access control
  	# page and use it to connect from an external network.
  		pass

	cursor = db.cursor()
	cursor.execute('SELECT 1 + 1')
	s = cursor.fetchall()

	return render_template('index.html', title = s , numbers = video_list_uploads)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
