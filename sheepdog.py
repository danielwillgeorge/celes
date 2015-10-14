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
  
  return channels_response["items"]