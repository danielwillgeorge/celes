import httplib2
import os
import sys
import itertools
import logging
import logging.config
import time

from apiclient.discovery import build_from_document
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from apiclient.http import BatchHttpRequest
from apiclient.errors import HttpError

# @Author Daniel George
# Sheepdog
# @Version 0.9.1


# This is Alex Moothart's channelId, for testing purposes
uniques = ['UCXqK1FO9yS8x7CMGkzLgJmA']

# These are unique commenters for Alex Moothart's channel, "The Moot Point" for testing purposes
# channels_list = ["UCdLWVR1C-hwcW4i558GeZ1A","UChuJTHTRhqBTsP3KCKyIieQ","UCTWdDAN_QrxWSumDs0z2bpA","UCQYfPb1c6_vDLAbGxSRUT5A","UC63nu_KBEVeVOlvfo-1D_Kw","UCiNUzLpahS0TjBgjobWdjNg","UCJY4haGpJ3Foymmdjp8S_Tg","UCOH3EONTobdSpSLz_S7W3lQ","UCHqg-aWTWbWHPpUliI2B-Vw","UCB6cbWd75lPW27rntPlLKow","UCcc_zG4pMLpuefQQs25e4bg","UC7Q6GvTqbiCIgqcNsdz-UEw","UCTCiI254D8lP1jNWYoc_RrA","UCM47dPWICE2zhPiMpa2Y-Gg","UCZ9E-vZyFw5YXL75u5PvrxA","UC6hwEfhOV8_kj61n7lk4wNg","UCoXu15iHZqmqIDGVsJlKucg","UC184MUWk-JadrboW8F9wFlQ","UCp1wRB2SHD-5PzL3Kt7crSg","UCUEt0vbfmLBvQEPDIFzAvkA","UCMR2NymnsFVloJxGQ7ILwdg","UC1ahXRNBL9vxmun4W2l8_uw","UCmZBrgkunOCGchMX9fnN96A","UCrlt-HmI8zeJaMhvqQ-MLSg","UC8yhMy7fVE86IfYRvo_PecQ","UC1snbc_vpLJgbDhOXxjbbPA","UCSeMnbw4jSnYNfzcvzvoVYw","UC7mi8f4ikb35Hz81nmNZmWw","UCfYkvwAOpt1zuCn2HkST93w","UCLYOZQ-Q9WDnCac0h7f46fw","UCD_ioRy-ICjX96iA_XZzM8g","UCFL6hdpOCq4bJ8cUsKga89w","UCUbUhCQXRrIoaVAFWvMOXUw","UCPD5r_CobvhHNTDLWVRhysg","UCuU8RHa4InGLMzoKtPBgVKw","UCKyO47S3Qqh7P6azvTPFpog","UCtK_ECnDfnd0z6wSOllMfFg","UCWkuh8bPrMthW49TFo5s1Mg","UCVKXsLBEleteY3Xl5yNIucg","UCvPM5oi1iwxb8DOziDkB-5w","UCGgvlOsxkN0ZqyYKqzTVzdQ","UCiuvBLPXSSefN15duJV36kA","UCxgZjzG87I3fXDcJCsJqlVQ","UChEgEbYmWFkVd46H_sBgajw","UC365Wb-Gk5Dxs0fqSzAmFLg","UCpqhnm8UqttRswwmI5ZWYew","UCWWRX7ZVmDbBhK1g13aDhlw","UCUWRrRcm1gYOpk_jK_svp-w","UCmu4-oVRRFDYk05DpyczotQ","UC9ZOJ3SGXFyOor6-4B1uRrA","UCocFdT9iSKx7osu0rnoNmGQ","UCtK_ECnDfnd0z6wSOllMfFg","UCsvJSMpnq9BP0HcstUASK6g","UC8nuvKdNBtY90ELrGvLSgSA","UCuKZh8xnED8Q6y3mf6Ie09A","UCwKMocTcYbYBm8tBV4kZ--w","UCFUr8bIlkMT1y9-OpT8Xn5g","UCVN_-AmwViHcPbDFhFhMv9Q","UCUMlFGNp4V6oiFCe_1WWaYA","UCkdFlxQe836q841RrDxueiA","UCewaP3rEFibp10FRGgufjZg","UCj-SrH1hCXqlGVC6GfXXvaQ","UCuh4cci7H6Ma66GMJ8s5Q5Q","UCnr1Rx6WF8UAeK00NhERrqA","UCi3qquNhMZWQtgSJiTN5AqA","UCTxTSEL69rrBzk9NAOZDl-g","UCFEZy2WPzGvqvIyr3nL6xBw","UCB7drWRe7B8Z6afod6agRWw","UCN8hZ0Q2bF9tlQ8Lqrfy-zw","UCgf3c6riglg3m9Oqofa7VDQ","UCzxoX7I_AOeMn-yzibquoMA","UCBCyDxn-iQBkx8Keq8aufHg","UCZDvO_3q_xlCzUEzp3DCzlg"]


channel_list = []
video_list = []
counter = []


# Set up a logger, formerly 'example.log'
logging.basicConfig(filename='sheepdog.log',level=logging.DEBUG) 
logger = logging.getLogger(__name__)


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google Developers Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for read-only access to the authenticated
# user's account, but not other types of account access.
#YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube" #.readonly
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SSL_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

with open("youtube-v3-discoverydocument.json", "r") as f:
  doc = f.read()
  youtube = build_from_document(doc, developerKey="AIzaSyBRgM5ARXMih_F9HviEUFYDpnkEmA4FPCs", http=credentials.authorize(httplib2.Http(cache=".cache")))

logger.info("Youtube build established.")

# Alternative "build" method to create youtube object
# youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey="AIzaSyBRgM5ARXMih_F9HviEUFYDpnkEmA4FPCs", http=credentials.authorize(httplib2.Http()))





# Part I - Retrieve the video uploads for a channel

def get_channels(youtube, channelId):
  """Retrieve the contentDetails part of the channel resource for the
     authenticated user's channel."""
  channels_response = youtube.channels().list(
    id=AUTH_USER_CHANNEL_ID,
    part="contentDetails"
  ).execute()
  
  return channels_response["items"]

def get_uploads(channel)
  video_list_uploads = []
  """From the API response, extract the playlist ID that identifies the list
     of videos uploaded to the authenticated user's channel."""
  try:
    uploads_list_Id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
  except KeyError:
    pass

  try:
	"""Retrieve the list of videos uploaded to the authenticated user's channel."""
	playlistitems_list_request = youtube.playlistItems().list(
	  playlistId=uploads_list_Id,
	  part="snippet",
	  maxResults=50
	)
  except NameError:
	pass

  try:
	while playlistitems_list_request:
	  try:
	  	playlistitems_list_response = playlistitems_list_request.execute()
	  except HttpError:
	  	pass
	  for playlist_item in playlistitems_list_response["items"]:
		video_id = playlist_item["snippet"]["resourceId"]["videoId"]
		video_list_uploads.append(video_id)
		
		# Returns the title of the video, if needed
		# title = playlist_item["snippet"]["title"]
		# Prints the title and videoId for testing, if needed
		# print "%s (%s)" % (title, video_id)
	  try:
	  	playlistitems_list_request = youtube.playlistItems().list_next(
	  	  playlistitems_list_request, 
	  	  playlistitems_list_response
	  	)
	  except HttpError:
	  	pass
  except NameError:
	pass

  return video_list_uploads


# Part II - get unique commenters for a channel
 
def get_comments(youtube, video_id, channel_id):
  """Retrieve the authors' channelIds of all of the comments, 
     of all of the uploaded videos, for the authorized user's channel."""
  global nextPageToken
  
  results = youtube.commentThreads().list(
      part="snippet", 
      videoId=video_id, 
      allThreadsRelatedToChannelId=AUTH_USER_CHANNEL_ID
    ).execute()

  nextPageToken = results.get("nextPageToken")

  for item in results["items"]:
    comment = item["snippet"]["topLevelComment"]
  	author = comment["snippet"]["authorDisplayName"]
  	authorChannelId = comment["snippet"]["authorChannelId"]
  	channel = authorChannelId.get("value")
  	
  	channel_list.append(channel)
  	
  return results["items"]
  
def get_more_comments(youtube, video_id, channel_id):
  global nextPageToken
  
  results = youtube.commentThreads().list(
    part="snippet", 
    videoId=video_id, 
    allThreadsRelatedToChannelId=AUTH_USER_CHANNEL_ID, 
    pageToken=nextPageToken
  ).execute()
  
  nextPageToken = results.get("nextPageToken")
  
  for item in results["items"]:
  	comment = item["snippet"]["topLevelComment"]
  	author = comment["snippet"]["authorDisplayName"]
  	
  	try:	
  		authorChannelId = comment["snippet"]["authorChannelId"]
  	except KeyError:
  		pass
  	
  	channel = authorChannelId.get("value")
  	
  	channel_list.append(channel)
  	
  return results["items"]
  








get_comments(youtube, None, AUTH_USER_CHANNEL_ID)

time.sleep(10)

logger.info("get_comments function successful.")

while nextPageToken:
	get_more_comments(youtube, None, AUTH_USER_CHANNEL_ID)
	time.sleep(10)
	
logger.info("get_more_comments function successful.")
logger.info("channel_list populated.")

uniques = list(set(channel_list))
uniques.sort()

logger.info("uniques list populated and sorted.")






# Part III

t0 = time.time()
for channelId in uniques:
	video_list = []
	#Retrieve the contentDetails part of the channel resource for the
	#authenticated user's channel.
	channels_response = youtube.channels().list(
      id=channelId, 
      part="contentDetails"
    ).execute()
	
	for channel in channels_response["items"]:
		try:
			uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["likes"]
		except KeyError:
			break
			
		try:
			print "Videos in list %s" % uploads_list_id
		except NameError:
			pass
		
		try:
			playlistitems_list_request = youtube.playlists().list(
			id=uploads_list_id, 
			part="contentDetails" 
			#fields="etag,nextPageToken,items(snippet(thumbnails/default,title,resourceId(videoId)))",
			#maxResults=50
			).execute()
			
			"""Return a count of all of the videoIds in the Likes playlist."""			
			for playlist_item in playlistitems_list_request["items"]:
				count = playlist_item["contentDetails"]["itemCount"]
				print "%s,%s" % (channelId, count)
		except NameError:
			break
			
# 		try:
# 			while playlistitems_list_request:
# 				try:
# 					playlistitems_list_response = playlistitems_list_request.execute()
# 				except HttpError:
# 					pass
# 				for playlist_item in playlistitems_list_response["items"]:
# 					title = playlist_item["snippet"]["title"]
# 					video_id = playlist_item["snippet"]["resourceId"]["videoId"]
# 					#print "%s (%s)" % (title, video_id)
# 					video_list.append([video_id, title])
# 				playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
# 				time.sleep(1)
# 			print "%s,%s" % (channelId, len(video_list))
# 		except NameError:
# 			pass
# 			
# t1 = time.time()
# total1 = t1-t0
# print total1


#### should take longer (this is the original)

batch = BatchHttpRequest()

t0 = time.time()
for channelId in uniques:
	video_list = []
	#Retrieve the contentDetails part of the channel resource for the
	#authenticated user's channel.
	channels_response = youtube.channels().list(
	  id=channelId, 
	  part="contentDetails"
	).execute()
	
	for channel in channels_response["items"]:
	  try:
	    uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["likes"]\
	  except KeyError:
	    break
			
		try:
			print "Videos in list %s" % uploads_list_id
		except NameError:
			pass
		
		try:
			playlistitems_list_request1 = youtube.playlistItems().list(
			playlistId=uploads_list_id, 
			part="snippet",
			pageToken="", 
			maxResults=50
			)
			
			playlistitems_list_request2 = youtube.playlistItems().list(
			playlistId=uploads_list_id, 
			part="snippet",
			pageToken="CDIQAA", 
			maxResults=50
			)
			
			playlistitems_list_request3 = youtube.playlistItems().list(
			playlistId=uploads_list_id, 
			part="snippet",
			pageToken="CGQQAA", 
			maxResults=50
			)
			
			playlistitems_list_request4 = youtube.playlistItems().list(
			playlistId=uploads_list_id, 
			part="snippet",
			pageToken="CJYBEAA", 
			maxResults=50
			)
			
		except NameError:
			break

		def list1(request_id,response,exception):
			print response
		
		def list2(request_id,response,exception):
			print response
		
		def list3(request_id,response,exception):
			print response
			
		def list4(request_id,response,exception):
			print response
			
		batch.add(playlistitems_list_request1, callback=list1)
		batch.add(playlistitems_list_request2, callback=list2)
		batch.add(playlistitems_list_request3, callback=list3)
		batch.add(playlistitems_list_request4, callback=list4)
		
		batch.execute(http=credentials.authorize(httplib2.Http(cache=".cache")))
			
t1 = time.time()
total2 = t1-t0
print total2

# 
# for line in video_list:
# 	counter.append(video_list.count(line))
# 	
# logger.info("counter list populated.")
# 
# for line in video_list:
# 	line.insert(0, counter[video_list.index(line)])
# 	try:
# 		line[1] = str(line[1])
# 		line[2] = str(line[2])
# 	except UnicodeEncodeError:
# 		pass
# 
# logger.info("video_list populated with counter.")
# 
# video_list.sort()
# 
# final = list(video_list for video_list,_ in itertools.groupby(video_list))
# 
# logger.info("final sorted and duplicates removed.")
# 
# final.sort()
# 
# #remove video ids belonging to initial user channel
# 
# for line in video_list_uploads:
# 	for i in final:
# 		if i[1] == line:
# 			final.remove(i)
# 			
# for line in final:
# 	print line
# 	
# logger.info("Script completed successfully.")