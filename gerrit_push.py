import os
import subprocess
import json
import slack
from gerrit_message import GerritMessage

cmd = 'ssh -p 29418 gowtham.alluri@gerrit.eng.nutanix.com gerrit query --comments NOT status:merged NOT status:abandoned owner:gowtham.alluri@nutanix.com --format=JSON'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()

output_str = output.decode("utf-8")
reviews = output_str.split('\n')

crs = []
for review in reviews:
    if len(review) > 0:
        rev_json = json.loads(review)
        print("Found another CR: \n")
        print(rev_json)
        crs.append(rev_json)

def send_message(chan):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    response = client.chat_postMessage(
        #channel='#random',
        channel=chan,
        text="Hello world!")
    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"
    print(response)


def send_gerrit_message(chan):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    gm = GerritMessage(chan, crs)

    msg = gm.get_message_payload()
    print("Sending following msg to channel %s:", chan)
    print(msg)

    response = client.chat_postMessage(**msg)
    assert response["ok"]
    print(response)

def get_im_list():
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    response = client.im_list()

    print(response)
    assert response["ok"]

#send_message("#general")
#send_gerrit_message("#general")

get_im_list()
#gowtham
send_gerrit_message('DTVQV3CP7')

#mayur
#send_gerrit_message('DTJAGQHB5')

#raghav
#send_gerrit_message('DTJAGQBC3')

#send_gerrit_message('@raghav.tulshibagwale')
#send_gerrit_message('@gowtham.alluri')




