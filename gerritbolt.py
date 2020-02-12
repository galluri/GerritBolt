import os
from slack import RTMClient

@RTMClient.run_on(event="message")
def say_hello(**payload):
  data = payload['data']
  web_client = payload['web_client']

  print(data)
  if 'subtype' in data:
    if 'bot_message' in data['subtype']:
      print("ignoring bot messages")
      return
 
  if 'text' in data:
    if 'retrigger' in data['text']:
      print(data['text'])
      channel_id = data['channel']
      thread_ts = data['ts']
      user = data['user']

      web_client.chat_postMessage(
        channel=channel_id,
        text=f"<@{user}>! the build has been retriggered",
        thread_ts=thread_ts
      )

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = RTMClient(token=slack_token)
rtm_client.start()
