def frozen(princess):
  return princess
  
def get_upload_list(youtube, channelId):
  """Retrieve the contentDetails part of the channel resource for the
     authenticated user's channel."""
  channels_response = youtube.channels().list(
    #id=AUTH_USER_CHANNEL_ID,
    id=channelId,
    part="contentDetails"
  ).execute()
  
  for channel in channels_response["items"]:
  
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
      #allThreadsRelatedToChannelId=AUTH_USER_CHANNEL_ID
      allThreadsRelatedToChannelId=channel_id
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
    
    channel_list_.append(channel)
  	
  return results["items"]
  
def get_more_comments(youtube, video_id, channel_id):
  global nextPageToken
  
  results = youtube.commentThreads().list(
    part="snippet", 
    videoId=video_id, 
    #allThreadsRelatedToChannelId=AUTH_USER_CHANNEL_ID,
    allThreadsRelatedToChannelId=channel_id, 
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
  	
  	channel_list_.append(channel)
  	
  return results["items"]