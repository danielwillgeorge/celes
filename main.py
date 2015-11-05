from flask import Flask, render_template, flash, Markup, json, jsonify, request
#import urllib
#import webapp2
import os

from apiclient.discovery import build
from apiclient.http import BatchHttpRequest
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue

#from google.appengine.ext import ext

import httplib2
import sys
import itertools
import logging
import logging.config
import time
import MySQLdb

from sheepdog import *
	
# from googleapiclient.discovery import build_from_document
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.file import Storage
# from oauth2client.tools import argparser, run_flow
# from apiclient.errors import HttpError

urlfetch.set_default_fetch_deadline(60)

# @Author Daniel George
# Sheepdog
# @Version 0.9.1

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

global channel_id
global channel_Id
global user
global nextPageToken

#video_list_uploads = ['Daniel','George']

channel_list = ['UCgJA3nqJEUZBkZivasUSdJg']
channel_list_ = []
#uniques = ['UCXqK1FO9yS8x7CMGkzLgJmA']
http = httplib2.Http(cache=memcache)

CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey="AIzaSyBRgM5ARXMih_F9HviEUFYDpnkEmA4FPCs") 


@app.route('/', methods=["GET", "POST"])
def hello():
	taskqueue.add()
	video_list_uploads = []

#	return render_template('index.html', title = "Princess Elsa" , numbers = video_list_uploads)
	
# 	storage = Storage("static/main.py-oauth2.json")
# 	credentials = storage.get()
# 	
# 	logging.debug(storage)
# 	logging.debug(credentials)
	
#	return render_template('index.html', title = "Princess Elsa" , numbers = video_list_uploads)
	
# 	json_data = open("static/youtube-v3-discoverydocument.json")
# 	doc = json.load(json_data)
	
	#http=credentials.authorize(httplib2.Http()))
   	
# 1st attempt with Google App Engine and
# the YouTube Data API.
# 	for channelId in channel_list:
# 
# 		channels_response = youtube.channels().list(id=channelId, part="contentDetails").execute()
# 	
# 		for channel in channels_response["items"]:
# 	
# 			try:
# 				uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["likes"]
# 			except KeyError:
# 				pass
# 
# 			try:
# 				playlistitems_list_request = youtube.playlistItems().list(playlistId=uploads_list_id, part="snippet", maxResults=50)
# 			except NameError:
# 				pass
# 		
# 			try:
# 				while playlistitems_list_request:
# 					try:
# 						playlistitems_list_response = playlistitems_list_request.execute()
# 					except HttpError:
# 						pass
# 						# Print information about each video.
# 					for playlist_item in playlistitems_list_response["items"]:
# 					#title = playlist_item["snippet"]["title"]
# 						video_id = playlist_item["snippet"]["resourceId"]["videoId"]
# 						video_list_uploads.append([video_id])
# 					try:
# 						playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
# 					except HttpError:
# 						pass
# 			except NameError:
# 				pass
				
				
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
	cursor.execute("""TRUNCATE sheepdog.videoIds_sample;""")
	db.commit()
	cursor.execute("""INSERT INTO sheepdog.videoIds_sample (videoId) VALUES ('TjqH3XiiUF8'),('Hc0ZPYhl_VE');""")
	db.commit()
	#s = cursor.fetchall()
	
	#cursor.execute("""INSERT INTO sheepdog.users (name, email) VALUES %s, %s;""", [request.json["name"], request.json["email"]])
	#db.commit()
	
	
	if request.method == "POST":
		r = request.get_json()
		name = r['name']
		email = r['email']
		token = r['access_token']
		logging.debug(token)
		
		cursor.execute("""INSERT INTO sheepdog.users (name, email) VALUES (%s,%s);""", [name, email])
		db.commit()
		
# 		youtube_ = 
		
# 		response = youtube.channels().list(access_token=token, mine="True", part="id").execute()
# 		logging.debug(response)
		#https://www.googleapis.com/youtube/v3/channels?access_token=&mine=True&part=id
# 		for channel in response["items"]:
# 			user_channelId = channel["id"]
		
	
	#time.sleep(2)
	
	#logging.debug(r['name'])
	
	#logging.debug(request.url)
	#logging.debug(r)
	#logging.debug(request.get_json()['name'])

	return render_template('index.html') #, title = s, numbers = video_list_uploads
	
@app.route('/user')
def user():
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
	cursor.execute("""TRUNCATE sheepdog.videoIds;""")
	db.commit()

	batch = BatchHttpRequest()
 	fr = frozen('Princess Elsa')
# 	uniques = ['UCXqK1FO9yS8x7CMGkzLgJmA']
# 	f = get_upload_list(youtube,"UCXqK1FO9yS8x7CMGkzLgJmA")
	
	for video_id in f:
	  cursor.execute("""INSERT INTO sheepdog.user_uploads (videoId) VALUES (%s);""", [video_id])
	  db.commit()
	
 	for videoId in f:
 	  request = get_comments(youtube, videoId, "UCXqK1FO9yS8x7CMGkzLgJmA")
 	  
	  def list1(request_id,response,exception):
		for item in response["items"]:
		  comment = item["snippet"]["topLevelComment"]
		  try:
		    authorChannelId = comment["snippet"]["authorChannelId"]
		    channel = authorChannelId.get("value")
		  except KeyError:
		    pass
		  channel_list_.append(channel)
		  
	  batch.add(request, callback=list1)

	batch.execute(http=http)
	
	uniques = list(set(channel_list_))
	uniques.sort()
	
	time.sleep(1)
 		
	
	video_list = []
	for channelId in uniques[:1]:
	  tokens = ["","CDIQAA","CGQQAA","CJYBEAA","CMgBEAA","CPoBEAA","CKwCEAA","CN4CEAA","CJADEAA","CMIDEAA","CPQDEAA","CKYEEAA", "CNgEEAA", "CIoFEAA", "CLwFEAA", "CO4FEAA", "CKAGEAA", "CNIGEAA", "CIQHEAA", "CLYHEAA", "COgHEAA", "CJoIEAA", "CMwIEAA", "CP4IEAA", "CLAJEAA", "COIJEAA", "CJQKEAA", "CMYKEAA", "CPgKEAA", "CKoLEAA", "CNwLEAA", "CI4MEAA", "CMAMEAA", "CPIMEAA", "CKQNEAA", "CNYNEAA", "CIgOEAA", "CLoOEAA", "COwOEAA", "CJ4PEAA", "CNAPEAA", "CIIQEAA", "CLQQEAA", "COYQEAA", "CJgREAA", "CMoREAA", "CPwREAA", "CK4SEAA", "COASEAA", "CJITEAA", "CMQTEAA", "CPYTEAA", "CKgUEAA", "CNoUEAA", "CIwVEAA", "CL4VEAA", "CPAVEAA", "CKIWEAA", "CNQWEAA", "CIYXEAA", "CLgXEAA", "COoXEAA", "CJwYEAA", "CM4YEAA", "CIAZEAA", "CLIZEAA", "COQZEAA", "CJYaEAA", "CMgaEAA", "CPoaEAA", "CKwbEAA", "CN4bEAA", "CJAcEAA", "CMIcEAA", "CPQcEAA", "CKYdEAA", "CNgdEAA", "CIoeEAA", "CLweEAA", "CO4eEAA", "CKAfEAA", "CNIfEAA", "CIQgEAA", "CLYgEAA", "COggEAA", "CJohEAA", "CMwhEAA", "CP4hEAA", "CLAiEAA", "COIiEAA", "CJQjEAA", "CMYjEAA", "CPgjEAA", "CKokEAA", "CNwkEAA", "CI4lEAA", "CMAlEAA", "CPIlEAA", "CKQmEAA", "CNYmEAA", ]

	  #Retrieve the contentDetails part of the channel resource for the
	  #authenticated user's channel.
	  channels_response = youtube.channels().list(
		id=channelId, 
		part="contentDetails"
	  ).execute()

	  for channel in channels_response["items"]:
		try:
		  likes_list_id = channel["contentDetails"]["relatedPlaylists"]["likes"]
		except KeyError:
		  break
		  
		playlist_item_count = youtube.playlistItems().list(
		playlistId=likes_list_id,
		part="id"
		).execute()
	
		count = playlist_item_count["pageInfo"]
		count = count.get("totalResults")
		n = count/50
		if count % 50 != 0:
		  n = n + 1
		
		for token in tokens[:n]:
  
		  try:
			playlistitems_list_request = youtube.playlistItems().list(
			  playlistId=likes_list_id, 
			  part="snippet",
			  pageToken="", 
			  maxResults=50)	  
		  except NameError:
			break

		  def list1(request_id,response,exception):
			for playlist_item in response["items"]:
			  video_id = playlist_item["snippet"]["resourceId"]["videoId"]
			  cursor.execute("""INSERT INTO sheepdog.videoIds (videoId) VALUES (%s);""", [video_id])
			  db.commit()
		  batch.add(playlistitems_list_request, callback=list1)
	
 	  batch.execute(http=http)
	  
	return render_template('user.html', title=fr)
	
@app.route('/_ah/queue/default', methods=["POST"])
def task():
  if request.method == "POST":
    f = get_upload_list(youtube,"UCXqK1FO9yS8x7CMGkzLgJmA")
    batch = BatchHttpRequest()
    
#     for video_id in f:
#       cursor.execute("""INSERT INTO sheepdog.user_uploads (videoId) VALUES (%s);""", [video_id])
#       db.commit()
    
    for videoId in f:
      r = get_comments(youtube, videoId, "UCXqK1FO9yS8x7CMGkzLgJmA")
      
      def list1(request_id,response,exception):
        for item in response["items"]:
          comment = item["snippet"]["topLevelComment"]
          try:
            authorChannelId = comment["snippet"]["authorChannelId"]
            channel = authorChannelId.get("value")
          except KeyError:
            pass
          channel_list_.append(channel)
          
      batch.add(r, callback=list1)
      
    batch.execute(http=http)
    
  uniques = list(set(channel_list_))
  uniques.sort()
#   
#   video_list = []
#   for channelId in uniques[:1]:
#     tokens = []
#     
#     channels_response = youtube.channels().list(
#       id=channelId,
#       part="contentDetails",
#     ).execute()
#     
#     for channel in channels_response["items"]:
#       try:
#         likes_list_id = channel["contentDetails"]["relatedPlaylists"]["likes"]
#       except KeyError:
#         break
    
    
  
    
  return 'string'

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
