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

reload(sys)
sys.setdefaultencoding("utf-8")

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
#   env = os.getenv('SERVER_SOFTWARE')
#   if (env and env.startswith('Google App Engine/')):
#   # Connecting from App Engine
#     db = MySQLdb.connect(
#     unix_socket='/cloudsql/peppy-linker-102423:daniel-george',
#     user='root',
#     db='sheepdog')
#   else:
#   # You may also assign an IP Address from the access control
#   # page and use it to connect from an external network.
#     pass
#   cursor = db.cursor()
  
  r = request.get_json()
  name = r['name']
  email = r['email']
  token = r['access_token']
  logging.debug(token)

#   cursor.execute("""INSERT INTO sheepdog.users (name, email) VALUES (%s,%s);""", [name, email])
#   db.commit()

  

  url = "https://www.googleapis.com/youtube/v3/channels?access_token=%s&mine=True&part=id" % token
  result = urlfetch.fetch(url)
  logging.debug(result.content)
  
  if token:
    logging.debug("Kate Upton")
    videoIds=["http://youtube.com/watch?v=WYodBfRxKWI",
    "http://youtube.com/watch?v=gkRDqSeCFes",
    "http://youtube.com/watch?v=4oEvM9-XhP8",
    "http://youtube.com/watch?v=h23oPnh1WJM",
    "http://youtube.com/watch?v=KWZGAExj-es",
    "http://youtube.com/watch?v=k9W5XWekhMI",
    "http://youtube.com/watch?v=2SexonKBB_U",
    "http://youtube.com/watch?v=diU70KshcjA",
    "http://youtube.com/watch?v=XLlSiCkKmDQ",
    "http://youtube.com/watch?v=sCxzaHC30Ec",
    "http://youtube.com/watch?v=lExW80sXsHs",
    "http://youtube.com/watch?v=Mt22-VMiR-Y",
    "http://youtube.com/watch?v=hlVBg7_08n0",
    "http://youtube.com/watch?v=389TMUtqX3E",
    "http://youtube.com/watch?v=ijvwFU4_5jk",
    "http://youtube.com/watch?v=e-ORhEE9VVg",
    "http://youtube.com/watch?v=HZJ2U-lYc30",
    "http://youtube.com/watch?v=3mKNyqK1CMI",
    "http://youtube.com/watch?v=kfpBmzatyX0",
    "http://youtube.com/watch?v=gNS04P8djk4"]
    channelIds=["UCudeRz9YntRrmKBSqnHyKGQ","UCGCPAOQDZa_TTTXDr5byjww","UCGCPAOQDZa_TTTXDr5byjww","UC9gFih9rw0zNCK3ZtoKQQyA","UCN9wHzrHRdKVzCSeV-5RuzA","UCudeRz9YntRrmKBSqnHyKGQ","UCIiBf-JbtCazHSFqXV4JgoA","UCeNfkWyfEXpZ8d1DmvwDt_w","UCfm4y4rHF5HGrSr-qbvOwOg",""]
    urls=["https://i.ytimg.com/vi/WYodBfRxKWI/default.jpg",
    "https://i.ytimg.com/vi/gkRDqSeCFes/default.jpg",
    "https://i.ytimg.com/vi/4oEvM9-XhP8/default.jpg",
    "https://i.ytimg.com/vi/h23oPnh1WJM/default.jpg",
    "https://i.ytimg.com/vi/KWZGAExj-es/default.jpg",
    "https://i.ytimg.com/vi/k9W5XWekhMI/default.jpg",
    "https://i.ytimg.com/vi/2SexonKBB_U/default.jpg",
    "https://i.ytimg.com/vi/diU70KshcjA/default.jpg",
    "https://i.ytimg.com/vi/XLlSiCkKmDQ/default.jpg",
    "https://i.ytimg.com/vi/sCxzaHC30Ec/default.jpg",
    "https://i.ytimg.com/vi/lExW80sXsHs/default.jpg",
    "https://i.ytimg.com/vi/Mt22-VMiR-Y/default.jpg",
    "https://i.ytimg.com/vi/hlVBg7_08n0/default.jpg",
    "https://i.ytimg.com/vi/389TMUtqX3E/default.jpg",
    "https://i.ytimg.com/vi/ijvwFU4_5jk/default.jpg",
    "https://i.ytimg.com/vi/e-ORhEE9VVg/default.jpg",
    "https://i.ytimg.com/vi/HZJ2U-lYc30/default.jpg",
    "https://i.ytimg.com/vi/3mKNyqK1CMI/default.jpg",
    "https://i.ytimg.com/vi/kfpBmzatyX0/default.jpg",
    "https://i.ytimg.com/vi/gNS04P8djk4/default.jpg"]
    urls_=["https://yt3.ggpht.com/-q3sXx_4QjjE/AAAAAAAAAAI/AAAAAAAAAAA/BVwUKML3cNQ/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-dDvEj5lMd9c/AAAAAAAAAAI/AAAAAAAAAAA/EULm0R9mEtk/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-bVdLMZDmXCk/AAAAAAAAAAI/AAAAAAAAAAA/SChajO2mTd8/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-34FbM3JM5Ck/AAAAAAAAAAI/AAAAAAAAAAA/qVlymUN44C8/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-ssT-qFQ2_UM/AAAAAAAAAAI/AAAAAAAAAAA/mqixgAYWk1E/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-PS6pgnf-7pY/AAAAAAAAAAI/AAAAAAAAAAA/QCBjV6iZUBI/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-SRcAgeuJbj8/AAAAAAAAAAI/AAAAAAAAAAA/YsJPiCWZUXY/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-EddJTwKC45c/AAAAAAAAAAI/AAAAAAAAAAA/dffQCcr3Tu4/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-E2z0657tkRo/AAAAAAAAAAI/AAAAAAAAAAA/Avs9FI5wSkA/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-w9XVuaKslpI/AAAAAAAAAAI/AAAAAAAAAAA/nhdbMmmKHGw/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-eMIdMVUl8OY/AAAAAAAAAAI/AAAAAAAAAAA/PrGrBG6Msjk/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-oJPyDp_XGV4/AAAAAAAAAAI/AAAAAAAAAAA/9Pi4ede175o/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-UFViqc6g5Io/AAAAAAAAAAI/AAAAAAAAAAA/XlanOV59iL4/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-_ya5gFNpWJs/AAAAAAAAAAI/AAAAAAAAAAA/memuFEGr4PQ/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-0A9XKZpCDjA/AAAAAAAAAAI/AAAAAAAAAAA/2TsFWukFl1Q/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-udmucUrJtoA/AAAAAAAAAAI/AAAAAAAAAAA/4XCFlSwE2lI/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-PR9CBGuWD-M/AAAAAAAAAAI/AAAAAAAAAAA/InqDjkxP5ss/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-8m4a8uXtWQs/AAAAAAAAAAI/AAAAAAAAAAA/badhAi9IqyI/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-u6o2bSQoW2M/AAAAAAAAAAI/AAAAAAAAAAA/6PiIY2suRck/s88-c-k-no/photo.jpg",
    "https://yt3.ggpht.com/-Pmv3XiLq6i0/AAAAAAAAAAI/AAAAAAAAAAA/PzA830mDGNo/s88-c-k-no/photo.jpg"]
    users_=["ConnorFranta",
    "IISuperwomanII",
    "TylerOakley",
    "JennaMarbles",
    "SiaVEVO",
    "TaylorSwiftVEVO",
    "JoeyGraceffa",
    "Paint",
    "SHAYTARDS",
    "PTXOfficial",
    "Ryan Lewis",
    "MyHarto",
    "JoshuaDTV",
    "MarkE Miller",
    "Troye Sivan",
    "TheNotAdam",
    "shep689",
    "Grace Helbig",
    "shane",
    "AdeleVEVO"]
    titles=["Coming Out",
    "If My Period Was A Person ft. Connor Franta",
    "So I Googled Myself...",
    "My 200th Video",
    "Sia - Elastic Heart feat. Shia LaBeouf & Maddie Ziegler (Official Video)",
    "So Relatable",
    "3 MILLION SUBS GIVEAWAY!",
    "After Ever After - DISNEY Parody",
    "Do you want to build a snowman? FROZEN",
    "Draw My Life- Jenna Marbles",
    "Evolution of Music - Pentatonix",
    "Guess The Body Part",
    "MACKLEMORE & RYAN LEWIS - SAME LOVE feat. MARY LAMBERT (OFFICIAL VIDEO)",
    "MY DRUNK KITCHEN: No Quitter Fritters",
    "Pet Peeves",
    "Taylor Swift - Blank Space",
    "The Photobooth Challenge (ft. MirandaSings) | Tyler Oakley",
    "The Proposal: Joshua and Colleen",
    "Twerking With Jessie J (#AskTyler #31) | Tyler Oakley",
    "Tyler Oakley Reacts to Teens React to Tyler Oakley"]
    #taskqueue.add()
    
    tags = ["London",
    "london",
    "the moot point",
    "alex moothart",
    "alex moothart vine",
    "eurovlog",
    "vlog",
    "vlogging",
    "europe",
    "europe vlog",
    "london vlog"]
    tags_ = ["London",
    "london",
    "the moot point",
    "alex moothart",
    "alex moothart vine",
    "eurovlog",
    "vlog",
    "vlogging",
    "europe",
    "europe vlog",
    "london vlog"]
    
    percents = ["40%",
    "40%",
    "20%",
    "20%",
    "20%",
    "10%",
    "10%",
    "10%",
    "5%",
    "5%"]
    percents_ = ["40%",
    "40%",
    "20%",
    "20%",
    "20%",
    "10%",
    "10%",
    "10%",
    "5%",
    "5%"]
    
    uploads = ["https://www.youtube.com/watch?v=-kQKr-Et25Q",
    "http://www.youtube.com/watch?v=j7Bgfqbcg4E",
    "http://www.youtube.com/watch?v=DC_rJLq3u_w",
    "http://www.youtube.com/watch?v=as8y7ou9ATI",
    "http://www.youtube.com/watch?v=-e1jVBqoebQ",
    "http://www.youtube.com/watch?v=ME89PcpgAMo",
    "http://www.youtube.com/watch?v=k8Wdk0GVzgA",
    "http://www.youtube.com/watch?v=nc4e9l2Y_-Q",
    "http://www.youtube.com/watch?v=ZVdW2ydy8s4",
    "http://www.youtube.com/watch?v=cDmDjP6E0Qc"
    ]
    upload_titles = ["Couples Halloween Costumes! (w/ Christine Sydelko)",
    "Estonia! (aka Narnia)",
    "Copenhagen!",
    "Oslo!",
    "London!",
    "Guess The Lyrics! (w/ Vero and Amy)",
    "Meeting My Family For The First Time",
    "Wedding Toast (Let It Go)",
    "THE WHIP Tutorial! (with MJ Riggins)",
    "IF/THEN Challenge: Steph Barkley!"
    
    ]
    photos = ["https://i.ytimg.com/vi/-kQKr-Et25Q/default.jpg",
    "https://i.ytimg.com/vi/j7Bgfqbcg4E/default.jpg",
    "https://i.ytimg.com/vi/DC_rJLq3u_w/default.jpg",
    "https://i.ytimg.com/vi/as8y7ou9ATI/default.jpg",
    "https://i.ytimg.com/vi/-e1jVBqoebQ/default.jpg",
    "https://i.ytimg.com/vi/ME89PcpgAMo/default.jpg",
    "https://i.ytimg.com/vi/k8Wdk0GVzgA/default.jpg",
    "https://i.ytimg.com/vi/nc4e9l2Y_-Q/default.jpg",
    "https://i.ytimg.com/vi/ZVdW2ydy8s4/default.jpg",
    "https://i.ytimg.com/vi/cDmDjP6E0Qc/default.jpg"
    
    ]
    descriptions = ["Here are the best and most original couples costumes for Halloween!\n----------------------------------------------------------------------------------------------------------------\nFOLLOW CHRISTINE!\n\nVINE: Christine Sydelko\nTWITTER: @csydelko\nINSTAGRAM: @csydelko\nSNAPCHAT: potatowithane\n----------------------------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "watch me explore Estonia!\n----------------------------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "Watch me explore Copenhagen!\n----------------------------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "Watch as I explore Oslo!\n----------------------------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "Watch me explore London!\n----------------------------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "Watch me try to guess the lyrics of Vero and Amy's new song \"The Abyss\"\n----------------------------------------------------------------------------------------------------------------\nFOLLOW THESE LESBIANS ON ALL THINGS SOCIAL MEDIA!\n\nYOUTUBE: Vero and Amy\nSPOTIFY: Vero and Amy\nINSTAGRAM: @veroandamy\nTWITTER: @veroandamy\nFACEBOOK: Vero & Amy\n----------------------------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "Here I meet two of my aunts for the first time and we go on a great dinner adventure! (ft. MJ Riggins and Mackenzie Becket)\n---------------------------------------------------------------------------------------------\nFOLLOW MJ ON ALL THINGS SOCIAL MEDIA!\n\nYOUTUBE: MJ Riggins\nVINE: MJ Riggins\nTWITTER: @MJRiggins\nINSTAGRAM: @MJRiggins\nSNAPCHAT: moe_murdah\n---------------------------------------------------------------------------------------------\nFOLLOW MACKENZIE ON ALL THINGS SOCIAL MEDIA!\n\nYOUTUBE: Mackenzie Becket\nVINE: Mackenzie Becket\nTWITTER: @mmmbecket\nINSTAGRAM: @mackenziebecket\nSNAPCHAT: ButterflyHugs\n---------------------------------------------------------------------------------------------                                                                FOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "I decided to give my mom and her husband a toast they would never be able to forget, so I wanted to sing an alternate version of \"Let It Go\" from Frozen. (Song starts around the 4:25 mark)\n---------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "In this video we teach you how to do the whip like the professionals. Because that's what we are. \n---------------------------------------------------------------------------------------------\nFOLLOW MJ ON ALL THINGS SOCIAL MEDIA!\n\nYOUTUBE: MJ Riggins\nVINE: MJ Riggins\nTWITTER: @MJRiggins\nINSTAGRAM: @MJRiggins\nSNAPCHAT: moe_murdah\n---------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nFACEBOOK: The Moot Point",
    "Here, we get to know the REAL Steph Barkley...and I LOVE HER.\n---------------------------------------------------------------------------------------------\nFOLLOW STEPH ON ALL THE SOCIAL MEDIA THINGS\n\nVINE: Steph Barkley\nTWITTER: @stephbarkley_3\nINSTAGRAM: @stephbarkley\nSNAPCHAT: barkdogg\nYOUTUBE: StephBarkleyAlterEgo\n---------------------------------------------------------------------------------------------\nFOLLOW ME IF YOU DARE (or just want to see more of me?)\n\nVINE: Alex Moothart\nTWITTER: @alexmoothart\nINSTAGRAM: @alexmoothart\nSNAPCHAT: amoot7\nTUMBLR: The Moot Point\nFACEBOOK: The Moot Point"
    
    ]
    
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