from flask import Flask, render_template, flash, Markup, json, jsonify, request, redirect, url_for
#import urllib
#import webapp2
import os

from apiclient.discovery import build
from apiclient.http import BatchHttpRequest
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch

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
#   taskqueue.add()
  video_list_uploads = []

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

  if request.method == "POST":
    r = request.get_json()
    name = r['name']
    email = r['email']
    token = r['access_token']
    logging.debug(token)
    
#     if token is None:
#       return render_template('index.html')
#     else:
#       return render_template('user.html')
    

    cursor.execute("""INSERT INTO sheepdog.users (name, email) VALUES (%s,%s);""", [name, email])
    db.commit()

    url = "https://www.googleapis.com/youtube/v3/channels?access_token=%s&mine=True&part=id" % token
    result = urlfetch.fetch(url)
    logging.debug(result.content)
    
#   if token is not None:
#     return redirect("http://www.google.com", code=302)
#   else:
  #logging.debug(request.url)
  
  fr="Princess Elsa"
  videoIds=["http://youtube.com/watch?v=WYodBfRxKWI","http://youtube.com/watch?v=z1PoNhYb3K4","http://youtube.com/watch?v=Kcwo_mhyqTw","http://youtube.com/watch?v=C7dxBlTC_9c","http://youtube.com/watch?v=PPdE3rbqf_Q","http://youtube.com/watch?v=4oEvM9-XhP8","http://youtube.com/watch?v=R1VUrOxRUsE","http://youtube.com/watch?v=3mKNyqK1CMI","http://youtube.com/watch?v=gkRDqSeCFes","http://youtube.com/watch?v=piW59SBH8KY"]
  channelIds=["UCudeRz9YntRrmKBSqnHyKGQ","UCGCPAOQDZa_TTTXDr5byjww","UCGCPAOQDZa_TTTXDr5byjww","UC9gFih9rw0zNCK3ZtoKQQyA","UCN9wHzrHRdKVzCSeV-5RuzA","UCudeRz9YntRrmKBSqnHyKGQ","UCIiBf-JbtCazHSFqXV4JgoA","UCeNfkWyfEXpZ8d1DmvwDt_w","UCfm4y4rHF5HGrSr-qbvOwOg",""]
  urls=["https://i.ytimg.com/vi/WYodBfRxKWI/default.jpg","https://i.ytimg.com/vi/z1PoNhYb3K4/default.jpg","https://i.ytimg.com/vi/Kcwo_mhyqTw/default.jpg","https://i.ytimg.com/vi/C7dxBlTC_9c/default.jpg","https://i.ytimg.com/vi/PPdE3rbqf_Q/default.jpg","https://i.ytimg.com/vi/4oEvM9-XhP8/default.jpg","https://i.ytimg.com/vi/R1VUrOxRUsE/default.jpg","https://i.ytimg.com/vi/3mKNyqK1CMI/default.jpg","https://i.ytimg.com/vi/gkRDqSeCFes/default.jpg",""]
  titles=["Video 1","Video 2","Video 3","Video 4","Video 5","So I Googled Myself...","Oops We're All Humans // Grace Helbig","The Proposal: Joshua and Colleen","If My Period Was A Person ft. Connor Franta","None"]
  #return render_template('user.html', videoIds=videoIds, channelIds=channelIds, urls=urls, titles=titles)

  return render_template('index.html', videoIds=videoIds, channelIds=channelIds, urls=urls, titles=titles)
  #return redirect("http://www.google.com", code=302)

@app.route('/user')
def user():
# 	env = os.getenv('SERVER_SOFTWARE')
# 	if (env and env.startswith('Google App Engine/')):
#   	# Connecting from App Engine
#   		db = MySQLdb.connect(
#     	unix_socket='/cloudsql/peppy-linker-102423:daniel-george',
#     	user='root',
#     	db='sheepdog')
# 	else:
#   	# You may also assign an IP Address from the access control
#   	# page and use it to connect from an external network.
#   		pass
# 
# 	cursor = db.cursor()
# 	cursor.execute("""TRUNCATE sheepdog.videoIds;""")
# 	db.commit()
# 
# 	batch = BatchHttpRequest()
#  	fr = frozen('Princess Elsa')
# # 	uniques = ['UCXqK1FO9yS8x7CMGkzLgJmA']
# # 	f = get_upload_list(youtube,"UCXqK1FO9yS8x7CMGkzLgJmA")
# 	
# 	for video_id in f:
# 	  cursor.execute("""INSERT INTO sheepdog.user_uploads (videoId) VALUES (%s);""", [video_id])
# 	  db.commit()
# 	
#  	for videoId in f:
#  	  request = get_comments(youtube, videoId, "UCXqK1FO9yS8x7CMGkzLgJmA")
#  	  
# 	  def list1(request_id,response,exception):
# 		for item in response["items"]:
# 		  comment = item["snippet"]["topLevelComment"]
# 		  try:
# 		    authorChannelId = comment["snippet"]["authorChannelId"]
# 		    channel = authorChannelId.get("value")
# 		  except KeyError:
# 		    pass
# 		  channel_list_.append(channel)
# 		  
# 	  batch.add(request, callback=list1)
# 
# 	batch.execute(http=http)
# 	
# 	uniques = list(set(channel_list_))
# 	uniques.sort()
# 	
# 	time.sleep(1)
#  		
# 	
# 	video_list = []
# 	for channelId in uniques[:1]:
# 	  tokens = ["","CDIQAA","CGQQAA","CJYBEAA","CMgBEAA","CPoBEAA","CKwCEAA","CN4CEAA","CJADEAA","CMIDEAA","CPQDEAA","CKYEEAA", "CNgEEAA", "CIoFEAA", "CLwFEAA", "CO4FEAA", "CKAGEAA", "CNIGEAA", "CIQHEAA", "CLYHEAA", "COgHEAA", "CJoIEAA", "CMwIEAA", "CP4IEAA", "CLAJEAA", "COIJEAA", "CJQKEAA", "CMYKEAA", "CPgKEAA", "CKoLEAA", "CNwLEAA", "CI4MEAA", "CMAMEAA", "CPIMEAA", "CKQNEAA", "CNYNEAA", "CIgOEAA", "CLoOEAA", "COwOEAA", "CJ4PEAA", "CNAPEAA", "CIIQEAA", "CLQQEAA", "COYQEAA", "CJgREAA", "CMoREAA", "CPwREAA", "CK4SEAA", "COASEAA", "CJITEAA", "CMQTEAA", "CPYTEAA", "CKgUEAA", "CNoUEAA", "CIwVEAA", "CL4VEAA", "CPAVEAA", "CKIWEAA", "CNQWEAA", "CIYXEAA", "CLgXEAA", "COoXEAA", "CJwYEAA", "CM4YEAA", "CIAZEAA", "CLIZEAA", "COQZEAA", "CJYaEAA", "CMgaEAA", "CPoaEAA", "CKwbEAA", "CN4bEAA", "CJAcEAA", "CMIcEAA", "CPQcEAA", "CKYdEAA", "CNgdEAA", "CIoeEAA", "CLweEAA", "CO4eEAA", "CKAfEAA", "CNIfEAA", "CIQgEAA", "CLYgEAA", "COggEAA", "CJohEAA", "CMwhEAA", "CP4hEAA", "CLAiEAA", "COIiEAA", "CJQjEAA", "CMYjEAA", "CPgjEAA", "CKokEAA", "CNwkEAA", "CI4lEAA", "CMAlEAA", "CPIlEAA", "CKQmEAA", "CNYmEAA", ]
# 
# 	  #Retrieve the contentDetails part of the channel resource for the
# 	  #authenticated user's channel.
# 	  channels_response = youtube.channels().list(
# 		id=channelId, 
# 		part="contentDetails"
# 	  ).execute()
# 
# 	  for channel in channels_response["items"]:
# 		try:
# 		  likes_list_id = channel["contentDetails"]["relatedPlaylists"]["likes"]
# 		except KeyError:
# 		  break
# 		  
# 		playlist_item_count = youtube.playlistItems().list(
# 		playlistId=likes_list_id,
# 		part="id"
# 		).execute()
# 	
# 		count = playlist_item_count["pageInfo"]
# 		count = count.get("totalResults")
# 		n = count/50
# 		if count % 50 != 0:
# 		  n = n + 1
# 		
# 		for token in tokens[:n]:
#   
# 		  try:
# 			playlistitems_list_request = youtube.playlistItems().list(
# 			  playlistId=likes_list_id, 
# 			  part="snippet",
# 			  pageToken="", 
# 			  maxResults=50)	  
# 		  except NameError:
# 			break
# 
# 		  def list1(request_id,response,exception):
# 			for playlist_item in response["items"]:
# 			  video_id = playlist_item["snippet"]["resourceId"]["videoId"]
# 			  cursor.execute("""INSERT INTO sheepdog.videoIds (videoId) VALUES (%s);""", [video_id])
# 			  db.commit()
# 		  batch.add(playlistitems_list_request, callback=list1)
# 	
#  	  batch.execute(http=http)

    fr="Princess Elsa"
    videoIds=["http://youtube.com/watch?v=WYodBfRxKWI","http://youtube.com/watch?v=z1PoNhYb3K4","http://youtube.com/watch?v=Kcwo_mhyqTw","http://youtube.com/watch?v=C7dxBlTC_9c","http://youtube.com/watch?v=PPdE3rbqf_Q","http://youtube.com/watch?v=4oEvM9-XhP8","http://youtube.com/watch?v=R1VUrOxRUsE","http://youtube.com/watch?v=3mKNyqK1CMI","http://youtube.com/watch?v=gkRDqSeCFes","http://youtube.com/watch?v=piW59SBH8KY"]
    channelIds=["UCudeRz9YntRrmKBSqnHyKGQ","UCGCPAOQDZa_TTTXDr5byjww","UCGCPAOQDZa_TTTXDr5byjww","UC9gFih9rw0zNCK3ZtoKQQyA","UCN9wHzrHRdKVzCSeV-5RuzA","UCudeRz9YntRrmKBSqnHyKGQ","UCIiBf-JbtCazHSFqXV4JgoA","UCeNfkWyfEXpZ8d1DmvwDt_w","UCfm4y4rHF5HGrSr-qbvOwOg",""]
    urls=["https://i.ytimg.com/vi/WYodBfRxKWI/default.jpg","https://i.ytimg.com/vi/z1PoNhYb3K4/default.jpg","https://i.ytimg.com/vi/Kcwo_mhyqTw/default.jpg","https://i.ytimg.com/vi/C7dxBlTC_9c/default.jpg","https://i.ytimg.com/vi/PPdE3rbqf_Q/default.jpg","https://i.ytimg.com/vi/4oEvM9-XhP8/default.jpg","https://i.ytimg.com/vi/R1VUrOxRUsE/default.jpg","https://i.ytimg.com/vi/3mKNyqK1CMI/default.jpg","https://i.ytimg.com/vi/gkRDqSeCFes/default.jpg",""]
    titles=["Video 1","Video 2","Video 3","Video 4","Video 5","Video 6","Video 7","Video 8","Video 9","Video 10"]
    return render_template('user.html', videoIds=videoIds, channelIds=channelIds, urls=urls, titles=titles)
    
@app.route('/_ah/queue/default', methods=["POST"])
def task():
  if request.method == "POST":
    f = get_upload_list(youtube,"UCXqK1FO9yS8x7CMGkzLgJmA")
    batch = BatchHttpRequest()
    
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
      db = MySQLdb.connect(
      unix_socket='/cloudsql/peppy-linker-102423:daniel-george',
      user='root',
      db='sheepdog')
      
      
    cursor = db.cursor()
    
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
  
  video_list = []
  likes_list_ids = []
  tokens = ["","CDIQAA","CGQQAA","CJYBEAA","CMgBEAA","CPoBEAA","CKwCEAA","CN4CEAA","CJADEAA","CMIDEAA","CPQDEAA","CKYEEAA", "CNgEEAA", "CIoFEAA", "CLwFEAA", "CO4FEAA", "CKAGEAA", "CNIGEAA", "CIQHEAA", "CLYHEAA", "COgHEAA", "CJoIEAA", "CMwIEAA", "CP4IEAA", "CLAJEAA", "COIJEAA", "CJQKEAA", "CMYKEAA", "CPgKEAA", "CKoLEAA", "CNwLEAA", "CI4MEAA", "CMAMEAA", "CPIMEAA", "CKQNEAA", "CNYNEAA", "CIgOEAA", "CLoOEAA", "COwOEAA", "CJ4PEAA", "CNAPEAA", "CIIQEAA", "CLQQEAA", "COYQEAA", "CJgREAA", "CMoREAA", "CPwREAA", "CK4SEAA", "COASEAA", "CJITEAA", "CMQTEAA", "CPYTEAA", "CKgUEAA", "CNoUEAA", "CIwVEAA", "CL4VEAA", "CPAVEAA", "CKIWEAA", "CNQWEAA", "CIYXEAA", "CLgXEAA", "COoXEAA", "CJwYEAA", "CM4YEAA", "CIAZEAA", "CLIZEAA", "COQZEAA", "CJYaEAA", "CMgaEAA", "CPoaEAA", "CKwbEAA", "CN4bEAA", "CJAcEAA", "CMIcEAA", "CPQcEAA", "CKYdEAA", "CNgdEAA", "CIoeEAA", "CLweEAA", "CO4eEAA", "CKAfEAA", "CNIfEAA", "CIQgEAA", "CLYgEAA", "COggEAA", "CJohEAA", "CMwhEAA", "CP4hEAA", "CLAiEAA", "COIiEAA", "CJQjEAA", "CMYjEAA", "CPgjEAA", "CKokEAA", "CNwkEAA", "CI4lEAA", "CMAlEAA", "CPIlEAA", "CKQmEAA", "CNYmEAA", ]

  def channelId_group(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))
  
  for group in channelId_group(uniques, 50):
    group = ','.join(group)
    
    channels_response = youtube.channels().list(
      id=group,
      part="contentDetails",
    ).execute()
    
    for channel in channels_response["items"]:
      try:
        likes_list_id = channel["contentDetails"]["relatedPlaylists"]["likes"]
        likes_list_ids.append(likes_list_id)
      except KeyError:
        pass

  for likes_list_id in likes_list_ids:
    taskqueue.add(queue_name="default", url="/google", params={"user":likes_list_id})
#     for token in tokens[:20]:
#       try:
#         playlistitems_list_request = youtube.playlistItems().list(
#           playlistId=likes_list_id,
#           part="snippet",
#           pageToken=token,
#           maxResults=50
#           )
#       except NameError:
#         pass
#         
#       def list1(request_id,response,exception):
#         for playlist_item in response["items"]:
#           video_id = playlist_item["snippet"]["resourceId"]["videoId"]
#           cursor.execute("""INSERT INTO sheepdog.videoIds (videoId) VALUES (%s);""", [video_id])
#           db.commit()
#       batch.add(playlistitems_list_request, callback=list1)
#       
#   batch.execute(http=http)
  
#@app.route("/")
#  task loop right here
  
  #Google Cloud SQL Query to pull top 10 videoIds
#   cursor.execute("""SELECT v.videoId FROM sheepdog.videoIds v WHERE v.videoId NOT IN (SELECT u.videoId FROM sheepdog.uploads u) GROUP BY v.videoId ORDER BY COUNT(v.videoId) DESC LIMIT 10""")
#   output = cursor.fetchall()
#   
#   for videoId in output:
#     results = youtube.videos().list(id=videoId, part="id,snippet").execute()
#     for item in results["items"]:
#       videoId_ = results["snippet"]["videoId"]
#       channelTitle_ = results["snippet"]["channelTitle"]
#       channelId_ = results["snippet"]["channelId"]
#       thumbnail = results["snippet"]["thumbnails"]["default"]["url"]
#       title_ = results["snippet"]["title"]
      
      
  
    
  return 'string'

@app.route("/google", methods=["POST"])
def Daniel(): 
  if request.method == "POST":
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
      db = MySQLdb.connect(
      unix_socket='/cloudsql/peppy-linker-102423:daniel-george',
      user='root',
      db='sheepdog')  
    cursor = db.cursor()
    tokens = ["","CDIQAA","CGQQAA","CJYBEAA","CMgBEAA","CPoBEAA","CKwCEAA","CN4CEAA","CJADEAA","CMIDEAA","CPQDEAA","CKYEEAA", "CNgEEAA", "CIoFEAA", "CLwFEAA", "CO4FEAA", "CKAGEAA", "CNIGEAA", "CIQHEAA", "CLYHEAA", "COgHEAA", "CJoIEAA", "CMwIEAA", "CP4IEAA", "CLAJEAA", "COIJEAA", "CJQKEAA", "CMYKEAA", "CPgKEAA", "CKoLEAA", "CNwLEAA", "CI4MEAA", "CMAMEAA", "CPIMEAA", "CKQNEAA", "CNYNEAA", "CIgOEAA", "CLoOEAA", "COwOEAA", "CJ4PEAA", "CNAPEAA", "CIIQEAA", "CLQQEAA", "COYQEAA", "CJgREAA", "CMoREAA", "CPwREAA", "CK4SEAA", "COASEAA", "CJITEAA", "CMQTEAA", "CPYTEAA", "CKgUEAA", "CNoUEAA", "CIwVEAA", "CL4VEAA", "CPAVEAA", "CKIWEAA", "CNQWEAA", "CIYXEAA", "CLgXEAA", "COoXEAA", "CJwYEAA", "CM4YEAA", "CIAZEAA", "CLIZEAA", "COQZEAA", "CJYaEAA", "CMgaEAA", "CPoaEAA", "CKwbEAA", "CN4bEAA", "CJAcEAA", "CMIcEAA", "CPQcEAA", "CKYdEAA", "CNgdEAA", "CIoeEAA", "CLweEAA", "CO4eEAA", "CKAfEAA", "CNIfEAA", "CIQgEAA", "CLYgEAA", "COggEAA", "CJohEAA", "CMwhEAA", "CP4hEAA", "CLAiEAA", "COIiEAA", "CJQjEAA", "CMYjEAA", "CPgjEAA", "CKokEAA", "CNwkEAA", "CI4lEAA", "CMAlEAA", "CPIlEAA", "CKQmEAA", "CNYmEAA", ]
    batch = BatchHttpRequest()
    user = request.form.get('user')
    
    for token in tokens[:20]:
      try:
        playlistitems_list_request = youtube.playlistItems().list(
          playlistId=user,
          part="snippet",
          pageToken=token,
          maxResults=50
          )
      except NameError:
        pass
        
      def list1(request_id,response,exception):
        for playlist_item in response["items"]:
          video_id = playlist_item["snippet"]["resourceId"]["videoId"]
          cursor.execute("""INSERT INTO sheepdog.videoIds (videoId) VALUES (%s);""", [video_id])
          db.commit()
      batch.add(playlistitems_list_request, callback=list1)
      
    batch.execute(http=http)
    
  return 'string'
  
@app.route('/terms')
def terms():
  return render_template('terms-of-service.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
