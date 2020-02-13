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
      text_str = data['text']
      tokens = text_str.split(" ")
      print(tokens[1])
      cmd = "ssh -p 29418 gowtham.alluri@gerrit.eng.nutanix.com gerrit review -m '\"trigger build\"' " + tokens[1] + ",1"
      print(cmd)
      os.system(cmd)
 
      channel_id = data['channel']
      thread_ts = data['ts']
      user = data['user']

      web_client.chat_postMessage(
        channel=channel_id,
        text=f"<@{user}>! the build has been retriggered",
        thread_ts=thread_ts
      )

@RTMClient.run_on(event="")
def retrigger(**payload):
  data = payload['data']
  print(data)


slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = RTMClient(token=slack_token)
rtm_client.start()
