from flask import Flask, render_template, flash, Markup, json, jsonify, request
#import urllib
#import webapp2
import os

from apiclient.discovery import build
from apiclient.http import BatchHttpRequest
from google.appengine.api import memcache
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
		access_token = r['access_token']
		
		cursor.execute("""INSERT INTO sheepdog.users (name, email) VALUES (%s,%s);""", [name, email])
		db.commit()
		
		
		
		
	
	#time.sleep(2)
	
	#logging.debug(r['name'])
	
	#logging.debug(request.url)
	#logging.debug(r)
	#logging.debug(request.get_json()['name'])

	return render_template('index.html') #, title = s, numbers = video_list_uploads
	
@app.route('/user')
def user():
	#f = frozen('Princess Elsa')
	uniques = ['UCXqK1FO9yS8x7CMGkzLgJmA']
	f = get_upload_list(youtube,"UCgJA3nqJEUZBkZivasUSdJg")
	#return render_template('user.html', title=f)
	
	get_comments(youtube, None, "UCXqK1FO9yS8x7CMGkzLgJmA")

	time.sleep(5)

	#logger.info("get_comments function successful.")

# 	while nextPageToken:
# 		get_more_comments(youtube, None, "UCXqK1FO9yS8x7CMGkzLgJmA")
# 		time.sleep(5)
	
	#logger.info("get_more_comments function successful.")
	#logger.info("channel_list populated.")

	#uniques = list(set(channel_list))
	#uniques.sort()
	
	#return render_template('user.html', uniques=f)

	#logger.info("uniques list populated and sorted.")
	
	batch = BatchHttpRequest()
	
	for channelId in uniques:
	  video_list = []
	  tokens = ["","CDIQAA","CGQQAA","CJYBEAA"]
	  #"CMgBEAA","CPoBEAA","CKwCEAA","CN4CEAA","CJADEAA","CMIDEAA","CPQDEAA","CKYEEAA", "CNgEEAA", "CIoFEAA", "CLwFEAA", "CO4FEAA", "CKAGEAA", "CNIGEAA", "CIQHEAA", "CLYHEAA", "COgHEAA", "CJoIEAA", "CMwIEAA", "CP4IEAA", "CLAJEAA", "COIJEAA", "CJQKEAA", "CMYKEAA", "CPgKEAA", "CKoLEAA", "CNwLEAA", "CI4MEAA", "CMAMEAA", "CPIMEAA", "CKQNEAA", "CNYNEAA", "CIgOEAA", "CLoOEAA", "COwOEAA", "CJ4PEAA", "CNAPEAA", "CIIQEAA", "CLQQEAA", "COYQEAA", "CJgREAA", "CMoREAA", "CPwREAA", "CK4SEAA", "COASEAA", "CJITEAA", "CMQTEAA", "CPYTEAA", "CKgUEAA", "CNoUEAA", "CIwVEAA", "CL4VEAA", "CPAVEAA", "CKIWEAA", "CNQWEAA", "CIYXEAA", "CLgXEAA", "COoXEAA", "CJwYEAA", "CM4YEAA", "CIAZEAA", "CLIZEAA", "COQZEAA", "CJYaEAA", "CMgaEAA", "CPoaEAA", "CKwbEAA", "CN4bEAA", "CJAcEAA", "CMIcEAA", "CPQcEAA", "CKYdEAA", "CNgdEAA", "CIoeEAA", "CLweEAA", "CO4eEAA", "CKAfEAA", "CNIfEAA", "CIQgEAA", "CLYgEAA", "COggEAA", "CJohEAA", "CMwhEAA", "CP4hEAA", "CLAiEAA", "COIiEAA", "CJQjEAA", "CMYjEAA", "CPgjEAA", "CKokEAA", "CNwkEAA", "CI4lEAA", "CMAlEAA", "CPIlEAA", "CKQmEAA", "CNYmEAA", ]

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
		
		logging.debug('Kate Upton is the hottest chick.')
		
		for token in tokens:
  
		  try:
			playlistitems_list_request = youtube.playlistItems().list(
			  playlistId=likes_list_id, 
			  part="snippet",
			  pageToken=token, 
			  maxResults=50
			)
			
			logging.debug("Kate Upton is so hot.")
			
		  except NameError:
			break

		  def list1(request_id,response,exception):
			for playlist_item in response["items"]:
			  video_id = playlist_item["snippet"]["resourceId"]["videoId"]
			  #print video_id
			  video_list.append(video_id)
			  
		  batch.add(playlistitems_list_request, callback=list1)
	
	  batch.execute(http=http)
	  
	return render_template('user.html', title=video_list)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
