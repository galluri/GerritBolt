import os
import slack
from gerrit_message import GerritMessage

def send_message(chan):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    response = client.chat_postMessage(
        #channel='#random',
        channel=chan,
        text="Hello world!")
    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"
    print(response)


#@slack.RTMClient.run_on(event='message')
#def say_hello(**payload):
#    data = payload['data']
#    web_client = payload['web_client']
#    rtm_client = payload['rtm_client']
#    if 'Hello' in data.get('text', []):
#        channel_id = data['channel']
#        thread_ts = data['ts']
#        user = data['user']
#
#        web_client.chat_postMessage(
#            channel=channel_id,
#            text=f"Hi <@{user}>!",
#            thread_ts=thread_ts
#        )
#
#slack_token = os.environ["SLACK_API_TOKEN"]
#rtm_client = slack.RTMClient(token=slack_token)
#rtm_client.start()

def send_gerrit_message(chan):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    gm = GerritMessage(chan, None)

    msg = gm.get_message_payload()
    print("Sending following msg to channel %s:", chan)
    print(msg)

    response = client.chat_postMessage(**msg)
    assert response["ok"]
    print(response)

send_message("#general")
send_gerrit_message("#general")

