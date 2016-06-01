# -*- coding: utf-8 -*-

"""
sheepdog.api
~~~~~~~~~~~~

This module implements the sheepdog API.

__author__ = "Daniel George"
__license__ = MIT, see LICENSE.txt for more details.
__version__ = 0.9.1

"""


from flask import Flask, render_template, flash, Markup, json, jsonify, request, redirect, url_for

from apiclient.discovery import build
from apiclient.http import BatchHttpRequest
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
# from google.appengine.ext import ext

# from googleapiclient.discovery import build_from_document
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.file import Storage
# from oauth2client.tools import argparser, run_flow
# from apiclient.errors import HttpError

import sys
import os
import itertools
import logging
import logging.config
import time
import MySQLdb
import httplib2
#import urllib
#import webapp2

from sheepdog import *

reload(sys)
sys.setdefaultencoding("utf-8")

urlfetch.set_default_fetch_deadline(60)

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

global channel_id
global channel_Id
global user
global nextPageToken

channel_list_ = []
http = httplib2.Http(cache=memcache)

CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey="AIzaSyBRgM5ARXMih_F9HviEUFYDpnkEmA4FPCs")

@app.route('/')
def root():
    return render_template('index.html', videoIds=[], channelIds=[], urls=[], titles=[], urls_=[], users_=[])
  
@app.route('/', methods=["POST"])
def root_():
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
  
    r = request.get_json()
    name = r['name']
    email = r['email']
    token = r['access_token']

#   cursor.execute("""INSERT INTO sheepdog.users (name, email) VALUES (%s,%s);""", [name, email])
#   db.commit()

    url = "https://www.googleapis.com/youtube/v3/channels?access_token=%s&mine=True&part=id" % token
    result = urlfetch.fetch(url)
    logging.debug(result.content)
  
  if token:
    videoIds=[]
    channelIds=[]
    urls=[]
    urls_=[]
    users_=[]
    titles=[]
    
    tags = []
    tags_ = []
    
    percents = []
    percents_ = []
    
    uploads = []
    upload_titles = []
    photos = []
    descriptions = []
    
    teni_videoIds = ["d5MNzjTiJuQ","qLV1a_611kA","BR0-yZ_-_5E","xpfNpdrgiqo","5xFCYvAN84I","dhz5QVOMFNo","BjJvxbXIzHY","JlOU98MHmWU","ujM39gK3W88","fLLvquQmWNI"]
    
    for teni_videoId in teni_videoIds:
      videos_list_request = youtube.videos().list(part="id, snippet", id=teni_videoId).execute()
    
    #keys = ["videoIds","channelIds","urls","urls_","users_","titles"]
    #values = [videoIds,channelIds,urls,urls_,users_,titles]
    keys = ["tags", "tags_","percents","percents_", "uploads", "upload_titles","photos","descriptions"]
    values = [tags, tags_, percents, percents_, uploads, upload_titles, photos, descriptions]
    res = dict(zip(keys, values))
    
    return jsonify(result=res)
    
  return "string"
    
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
    
    for video_id in f:
      cursor.execute("""INSERT INTO sheepdog.user_uploads (videoId) VALUES (%s);""", [video_id])
      db.commit()
    
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
  
  #Google Cloud SQL Query to pull top 10 videoIds
#   cursor.execute("""SELECT v.videoId FROM sheepdog.videoIds v WHERE v.videoId NOT IN (SELECT u.videoId FROM sheepdog.user_uploads u) GROUP BY v.videoId ORDER BY COUNT(v.videoId) DESC LIMIT 10""")
#   output = cursor.fetchall()

#   logging.debug(output)
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
def task_(): 
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
  
@app.route('/privacy')
def privacy():
  return render_template('privacy.html')
  
@app.route('/contact')
def contact():
  return render_template('contact.html')
  
@app.route('/support')
def support():
  return render_template('support.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404