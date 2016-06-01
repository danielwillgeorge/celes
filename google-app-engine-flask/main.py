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
    
    tags = [ "Teni",
 "Teni Panosian",
 "Beauty Hacks",
 "Makeup",
 "Easy Makeup Tutorial",
 "Eye Makeup",
 "Cosmetics",
 "Makeup Tutorials",
 "Makeup Tips",
 "Beauty Tips"]
    tags_ = [ "Teni",
 "Teni Panosian",
 "Beauty Hacks",
 "Makeup",
 "Easy Makeup Tutorial",
 "Eye Makeup",
 "Cosmetics",
 "Makeup Tutorials",
 "Makeup Tips",
 "Beauty Tips"]
    
    percents = ["100%",
    "100%",
    "100%",
    "100%",
    "100%",
    "100%",
    "80%",
    "80%",
    "80%",
    "80%"]
    percents_ = ["100%",
    "100%",
    "100%",
    "100%",
    "100%",
    "100%",
    "80%",
    "80%",
    "60%",
    "60%"]
    
    uploads = ["https://www.youtube.com/watch?v=d5MNzjTiJuQ",
    "http://www.youtube.com/watch?v=qLV1a_611kA",
    "http://www.youtube.com/watch?v=BR0-yZ_-_5E",
    "http://www.youtube.com/watch?v=xpfNpdrgiqo",
    "http://www.youtube.com/watch?v=5xFCYvAN84I",
    "http://www.youtube.com/watch?v=dhz5QVOMFNo",
    "http://www.youtube.com/watch?v=BjJvxbXIzHY",
    "http://www.youtube.com/watch?v=JlOU98MHmWU",
    "http://www.youtube.com/watch?v=ujM39gK3W88",
    "http://www.youtube.com/watch?v=fLLvquQmWNI"
    ]
    upload_titles = ["Current Everyday Makeup Routine | Teni Panosian",
    "Snapchat Q+A (Part I) | Teni Panosian",
    "Room Tour: My Workspace | Teni Panosian",
    "Gray Smokey Eye Makeup Tutorial | Teni Panosian",
    "Glitter Eye Makeup Tutorial | Winged Eyeliner Makeup | Teni Panosian",
    "Best Lip Colors for Winter | Teni Panosian",
    "Holiday Makeup | Winged Eyeliner + Red Lips  | Teni Panosian",
    "Brown Smokey Eye Makeup Tutorial | Teni Panosian",
    "Travel Diary: Turks and Caicos | Beauty Blogger | Teni Panosian",
    "Skincare Issues | Teni Panosian"
    
    ]
    photos = ["https://i.ytimg.com/vi/d5MNzjTiJuQ/default.jpg",
    "https://i.ytimg.com/vi/qLV1a_611kA/default.jpg",
    "https://i.ytimg.com/vi/BR0-yZ_-_5E/default.jpg",
    "https://i.ytimg.com/vi/xpfNpdrgiqo/default.jpg",
    "https://i.ytimg.com/vi/5xFCYvAN84I/default.jpg",
    "https://i.ytimg.com/vi/dhz5QVOMFNo/default.jpg",
    "https://i.ytimg.com/vi/BjJvxbXIzHY/default.jpg",
    "https://i.ytimg.com/vi/JlOU98MHmWU/default.jpg",
    "https://i.ytimg.com/vi/ujM39gK3W88/default.jpg",
    "https://i.ytimg.com/vi/fLLvquQmWNI/default.jpg"
    
    ]
    descriptions = ["I’ve updated my simple everyday makeup routine! A lot of you ask for this type of natural makeup look so I hope you like it. :) Be sure to give the video a ‘like’ a subscribe: http://bit.ly/subtoteni\n \nFollow me everywhere! \nOfficial site: http://missmaven.com/\nInstagram: @tenipanosian\nTwitter: @TeniPanosian\nFacebook: http://www.facebook.com/teni.panosian\nSnapchat: TeniPanosian\n \nP R O D U C T S\n \nMarc Jacobs Perfecting Coconut Face Primer\nNARS Velvet Matte Skin Tint in Medium 1 St. Moritz - http://bit.ly/1lSIWuC\nNARS Radiant Creamy Concealer in Ginger http://bit.ly/1SMfRz2\nLaura Mercier Translucent Powder\nMilani Baked Blush in Dolce Pink\ntheBalm Betty LouManizer bronzing powder\nJouer Luminizing Liquid Highlighter in Golden Light\nColourPop eyeshadows:\n⇢ Truth\n⇢ As If\n⇢ Crimper\nHourglass 1.5mm eyeliner in black\nMaybelline The Falsies Push Up Drama Mascara\nHourglass Arch Brow Sculpting Pencil in Dark Brunette\nEstee Lauder lip gloss in Vinyl Rose\n \n \n \nFTC: The only thing sponsored in this video is the NARS Velvet Matte Skin tint which, of course, is 100% Teni-approved. :)\n \n\n♥ About Teni Panosian♥\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!",
    "Here's my very first Snapchat Q+A! This was so much fun and since there were more questions than I could answer in one video, there's a part II coming next week!!! Thanks to everyone for sending in your questions :) And if you don't follow me on Snapchat here's my username: tenipanosian\n\n\nOne of the questions was about the equipment I shoot with, here are the specific names:\n- Canon 5D Mark III\n- Kino Flo 4ft 4 bank lamp kit\n- Sony LMD-1510W Multi format LCD Monitor 15.6\"\n- 24-70mm Canon lens\n\n\nFollow me everywhere! \nOfficial site: http://missmaven.com/\nIG: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\nFB:https://www.facebook.com/teni.panosian\nPinterest: https://www.pinterest.com/missmavendotcom/\n\n\n\n\nAbout Teni Panosian\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!",
    "I'm so excited to share the first part of my house tour! I hope you guys love what I did with the space... Follow me on snapchat for more footage of the room and to see how the remodeling is coming along on the main house! Snapchat username: tenipanosian\n\n♥ Follow me everywhere! ♥\nOfficial site: http://missmaven.com/\nIG: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\nFB:https://www.facebook.com/teni.panosian\nPinterest: https://www.pinterest.com/missmavendotcom/\n\nFURNITURE AND DECOR DETAILS:\nKendall Sofa: World Market (online)\nSilvery blue throw pillow: West Elm (in store)\nBeaded blue throw pillow: Home Goods\nSafavieh Rug: Wayfair.com\nMarble top coffee table: CB2 (in store and online)\nGold pineapple vase: CB2 (in store)\nAgate coasters: Anthropologie (online)\nFaux Shearling custom chair: Etsy https://goo.gl/BQMziM\nChrome wall mount bookcases: CB2 (in store and online)\nChrome skull: CB2 (in store)\nBrass gallery frames: CB2 (in store and online)\nTripod floor lamp: West Elm (online)\nGold pouf: RachelGeorge.com\nFolding table with gold legs and white tray: CB2 (in store)\nFloor mirror: Home Goods\nMarble and gold end table: RachelGeorge.com\nCopper end table and mint vase: CB2 (in store)\nDesk: Bernhardt (online at Horchow)\nMetallic gold makeup brush print: Glam-prints.com\nAcrylic chair: Retrofurnish\nFaux shearling throw: Ikea\nBrass desk lamp and brass lantern: West Elm (in store)\nDesk accessories: RachelGeorge.com\nMakeup organizer drawers: Ikea *** this was marked as a last chance item so I don't know if they will sell it for much longer!\n\n\nThe floors are from a store in Glendale, CA called ADCO. They are a laminate variety and the color is called Sea Smoke. \n\n\nFTC: This is not a sponsored video. \n\n\n\n♥ About Teni Panosian♥\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!",
    "Here's a smokey eye makeup tutorial using gray and silver tones for a more soft and natural makeup look! Hope you love it :) Please 'like' and subscribe! ⇢ http://bit.ly/subtoteni\n\n♥ Follow me everywhere! ♥\nOfficial site: http://missmaven.com/\nInstagram: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\n\nP R O D U C T S\n\nMarc Jacobs Perfecting Coconut Face Primer\nMake Up For Ever Ultra HD Foundation in Y385\nNARS Radiant Creamy Concealer in Ginger http://bit.ly/1QYwW8w\nMake Up For Ever Ultra HD Stick Foundation in Y505 (contour)\nLaura Mercier Translucent Powder\nHourglass blush in Luminous Flush\nGuerlain Terracotta Bronzer\ntheBalm Betty LouManizer mixed with Mary LouManizer\nToo Faced Shadow Insurance Primer\nNEW Nars Narsissist Eyeshadow Palette ⇢ http://bit.ly/1mh4j9S\n⇢ Cream Bisque\n⇢ Cafe au Lait\n⇢ Amethyst Ash\n⇢ Black Truffle\n⇢ Shimmering Taupe Cashmere\n⇢ Golden Starlight\nHourglass 1.5mm eyeliner in black\nMaybelline The Falsies Push Up Drama Mascara\nLORAC PRO Brow Pencil in Brunette\nMotives Cosmetics lipstick in Kissable\n\n\n\n\nFTC: The only thing sponsored in this video is the NARS eyeshadow palette but, let's be honest, it's an awesome palette! :P \n\n\n♥ About Teni Panosian♥\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!",    
    "Glitter eye makeup is the perfect look for New Year’s Eve! So I created this bold winged eyeliner look with glitter... I hope you love this video and have a wonderful start to 2016. :) Please give the video a ‘like’ and subscribe for more! ⇢ http://bit.ly/subtoteni\n\n⇢ Follow me everywhere! \nOfficial site: http://missmaven.com/\nIG: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\nFB:https://www.facebook.com/MissMaven\nPinterest: https://www.pinterest.com/missmavendotcom/\n\nP R O D U C T S\n\nMarc Jacobs Undercover Perfecting Coconut Face Primer\nMake Up For Ever Full Cover Concealer in Sand 7\nNARS Radiant Creamy Concealer in Ginger\nMake Up For Ever Ultra HD Foundation in Y385\nMake Up For Ever Ultra HD Stick Foundation in Y505 (contour)\nCharlotte Tilbury Airbrush Flawless Powder in Medium\nGuerlain Terracotta Bronzing Powder\nCharlotte Tilbury Cheek to Chic Blush in First Love\nBenefit Stay Don’t Stray Eyeshadow Primer\nTarte Tartelette 2 In Bloom Eyeshadow Palette\n⇢ Flower Child\n⇢ Smarty Pants\n⇢ Jetsetter\n⇢ Activist\nTarte Tarteist Clay Liner\nToo Faced Glitter Glue\nMake Up For Ever Glitter in N15 Midnight Glow\nMaybelline Push Up Falsies Mascara\nHouse of Lashes Pixie Luxe lashes\nAnastasia Beverly Hills Brow Wiz in Soft Brown\nBH Cosmetics Stripped lip liner\nEstee Lauder lip gloss in Vinyl Rose\n\nB R U S H E S \n\nMorphe M320\nEcoTools Large Powder Brush\nNARS Yachiyo Brush\nMorphe M441\nAnastasia Beverly Hills Double Ended Brush (from the Shadow Couture palette)\nSephora Collection PRO Angled Eyeliner Brush\nMorphe M202\n\n\nTips for using glitter:\n⇢ If you get any on your face, just take scotch tape and lightly press it against your face and it’ll pick up the glitter.\n⇢ If you don’t have glitter glue, you can also mix one part eyelash glue with one part water and it’ll work just as well. \n\n\nFTC: This is not a sponsored video. \n\nMusic is from Epidemic Sound.\n\n\n♥ About Teni Panosian♥\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!",    
    "Here are my top 6 lip colors for winter! These all turned out to be matte lipsticks just because I feel like they look so good in the winter, I hope you like them! Please like and subscribe :) http://bit.ly/subtoteni\n\n♥ Follow me everywhere! ♥\nOfficial site: http://missmaven.com/\nIG: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\nFB:https://www.facebook.com/MissMaven\nPinterest: https://www.pinterest.com/missmavendotcom/\n\nPRODUCTS:\n\nGirlactik Matte Lip Paint in Posh\n\nColourPop Ultra Matte Liquid Lipstick in Times Square\n\nStila Stay All Day Liquid Lipstick in Ricco\n\nJeffree Star Velour Liquid Lipstick in Unicorn Blood\n\nKat Von D Everlasting Liquid Lipstick in Damned\n\nLime Crime Velvetine in Salem\n\n\n\nFTC: This is not a sponsored video.\n\n\n\n\n♥ About Teni Panosian♥\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!",    
    "Here comes a holiday makeup tutorial! I paired a sharp winged eyeliner look with some bright red lips for a festive and classic makeup look. Hope you love it! Please like and subscribe :)  http://bit.ly/subtoteni\n\n\nFollow me everywhere! \nOfficial site: http://missmaven.com/\nIG: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\nFB:https://www.facebook.com/MissMaven\nPinterest: https://www.pinterest.com/missmavendotcom/\n\n\nProducts:\nJouer Anti-Blemish Matte Primer\nNARS All Day Luminous Weightless Foundation in Stromboli\nBeauty Blender\nNARS Raidant Creamy Concealer in Ginger and Custard\nMake Up For Ever Ultra HD stick foundation in Y505 (contour)\nLaura Mercier Translucent Powder\nTarte Bling It On Amazonian Clay blush palette, Beaming\ntheBalm Betty LouManizer bronzer\nGirlactik Face Glow in Lustre\nUrban Decay All Nighter Setting Spray\nBenefit Stay Don't Stray Eyeshadow Primer\nMakeup Geek eyeshadows\n⇢ beaches n creme\n⇢ creme brulee\n⇢ latte\n⇢ americano\nColourPop Super Shock Shadow in Crimper\nTarte Tarteist Clay Liner \nLancome Grandiose Mascara\nHouse of Lashes \"Noir Fairy\" false lashes\nAnastasia Beverly Hills Brow Wiz in Soft Brown\nColourPop Lippie Liner in Chi Chi\nTarte Tarteist Lip Paint in Cray Cray *** This is going to be available  on 12/15!! \n\n\nBrushes:\nEcoTools Stippling Brush\nEcoTools Round Powder\nMorphe M438\nTarte Highlight Brush\nMorphe M441\nElaina Badro blending brush\nSephora PRO Angled Liner Brush\nIT Cosmetics double ended shadow and smudge brush\n\n\n\n\n\n\nFTC: This is not a sponsored video. \n\n\n\n♥ About Teni Panosian♥\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!\n\nMusic by Epidemic Sound.",    
    "Here's a brown smokey eye makeup look for ya! I kept the colors neutral but made the eye makeup pretty dramatic. I hope you love it! Please like and subscribe if you do :) ⇢ http://bit.ly/subtoteni\n\nFollow me everywhere:\nOfficial site: http://missmaven.com/\nIG: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\nFB:https://www.facebook.com/MissMaven\nPinterest: https://www.pinterest.com/missmavendotcom/\n\nProducts:\n\nTarte Home For The Holidaze Set\n⇢ Pop the Cork\n⇢ Feeling Fizzy\n⇢ Chocolate Fountain\n⇢ LBD\n⇢ Swanky (this was the blush in the palette)\nHourglass 1.5mm pencil in Black\nLancome Grandiose Mascara\nHouse of Lashes falsies in “Noir Fairy”\nMake Up For Ever Nourishing Primer\nToo Faced Born This Way Foundation in Warm Beige\nBeauty Blender\nMaybelline Age Rewind Dark Circle Eraser in Medium\nMotives Sculpt Series contour palette in Fire\nCharlotte Tilbury Airbrush Perfecting Powder\nBetty LouManizer bronzer\nAnastasia Beverly Hills Brow Wiz in Soft Brown\nColourPop lip pencil in Tootsi\nLORAC Alter Ego Lipstick in Visionary\nLORAC lip gloss in Visionary\n\nBrushes:\n\nMorphe 441\nIT Cosmetics Double Ended shadow and smudge brush\nDouble ended shadow brush from the Anastasia Beverly Hills Shadow Couture palette\nE55\nSmall blending brush from the Tarte Holiday Collection\nFluffy highlight brush from the Tarte Holiday Collection\n\nFTC: This is not a sponsored video. \n\n\nAbout Me\n\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!",    
    "Follow me as I show you my travels to Turks and Caicos with some of my pals from YouTube and Instagram! A big thank you to Tarte Cosmetics for including me on this trip, and I hope you all enjoy this vlog! Give the video a like and subscribe, pretty please :) http://bit.ly/subtoteni\n\nCheck out Potcake Place Rescue, they were so awesome and we learned a lot about the stray animals on the islands: http://www.potcakeplace.com/\n\nWhat I wore:\n\nDay 1 - Arrival\nShorts: The Gap\nStriped blouse: Zara\n\nDay 2 - Sailing\nBlack wrap-around swim suit: L*Space\nSunglasses: Hawkers\n(we had dinner that night and I wore a cute outfit that I'll post to Instagram!!)\n\nDay 3 - Tarte House & Bonfire\nBlack and bronze swimsuit: Victoria's Secret\nBlack and white dress: L*Space\nBlack cage sandals: Schutz\nSunglasses: Quay Australia\n(the red lippie is unreleased from Tarte!!)\n\nDay 4 - Trapeze & Conch Shack dinner\nLeotard: One Rad Girl\nDenim cutoffs: One Teaspoon\nStriped sleeveless tee: \nShorts: The Gap\n\nDay 5 - Departure\nWhite and gold one-piece swimsuit: Victoria's Secret (a few years old)\n\nHOMIES IN THIS VIDEO: (Youtube and Instagram)\nMaryam - @maryamnyc\nDenise - @makeupbydenise\nPatrick - https://www.youtube.com/theepatrickstarrr\nDesi - https://www.youtube.com/desireeperkinsmakeup\nKaty - https://www.youtube.com/lustrelux\nChrisspy - https://www.youtube.com/chrisspymakeup\nChristen - https://www.youtube.com/christendominique\nTamana - @dressyourface\nNicole - @nicoleconcillio\nGina - @ginashkeda\nShayla - @makeupshayla\nKaren - @iluvsarahii\nHrush - @styledbyhrush\nRachel - https://www.youtube.com/rclbeauty101\nLaura - @laura _g143\n\n*** THANK YOU *** to my boyfriend, Chris, for taking the time to shoot this for me! You are the best!!\n\n\n♥ Follow me everywhere! ♥\nOfficial site: http://missmaven.com/\nIG: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\nFB:https://www.facebook.com/MissMaven\nPinterest: https://www.pinterest.com/missmavendotcom/\n\n\nFTC: This is not a sponsored video.\n\n\n♥ About Teni Panosian♥\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!\n\n\nMUSIC: \nTrack 1 is from https://www.youtube.com/ninety9lives and track 2 is from premiumbeat.com.",
    "Instead of an updated skincare routine I decided to address specific skincare issues that many of you ask about and recommend the best products. We're talking texture, wrinkles, pigmentation, and more! Please like and subscribe! http://bit.ly/subtoteni\n\n\n♥ Follow me everywhere! ♥\nOfficial site: http://missmaven.com/\nIG: @tenipanosian\nTwitter: @TeniPanosian\nSnapchat: TeniPanosian\nFB:https://www.facebook.com/MissMaven\nPinterest: https://www.pinterest.com/missmavendotcom/\n\n\nPRODUCTS:\n\n--DARK CIRCLES--\nShiseido White Lucent Anti-Dark Circles Eye Cream\n\n--TEXTURE ISSUES/UNEVENNESS--\nMurad Intensive-C Radiance Peel (Mild)\nOle Henriksen Lemon Strip Flash Peel (Extra Strong)\nDr. Dennis Gross Alpha Beta Peel Pads (Strong)\n\n--PIGMENTATION--\nMurad Rapid Age Spot & Pigment Lightening Serum\n\n--FINE LINES/WRINKLES--\nDermalogica Ultra Smoothing Eye Serum\n\n--BEST DRUGSTORE OPTIONS--\nNeutrogena Rapid Wrinkle Repair Serum\nNeutrogena Rapid Wrinkle Repair Night Cream\nOlay Regenerist Micro Sculpting Cream\n\n**** PROMO CODE FOR MURAD ****\n\nUse code TENI20 to get 20% off at Murad.com on any of your favorite products, including the Rapid Lightening Regimen. May be used one time per customer and some restrictions may apply. Happy shopping!!\n\n\nFTC: The only product in this video that is sponsored is the Murad Rapid Pigment Lightening Serum, though you guys know I've been using and loving Murad products for years and as a result I've built an ongoing relationship with the brand. As always, all opinions are my own and all products are tested by me!\n\n\n♥ About Teni Panosian♥\nHi! I’m Teni Panosian the beauty blogger behind the style and beauty blog MissMaven.com, and welcome to my official YouTube channel! If it's makeup, beauty, skincare, hair, and style you're looking for, you've come to the right makeup channel! I’m not a makeup artist; I’m coming to you as another consumer like yourself… I just happen to be an extremely well-informed cosmetics buyer with great makeup tips. From beauty hacks, makeup tips, beauty advice, makeup hauls, to beauty product reviews I’ve got something for everyone. Whether you’re looking for eye makeup tutorials, full coverage makeup tutorials, or how to apply matte lipstick, let me show you my makeup routine. While my strength is in beauty, you’ll also find a sprinkle of fashion, lifestyle, and wellness content here. Check out my style tips in my what to wear videos and my personal vlogs as I travel and live my crazy life. Thanks for checking out my channel. :) I hope you enjoy!"    
    ]
    
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