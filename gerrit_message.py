import time
import datetime

class GerritMessage:
    """Constructs gerrit message consisting of list of codereview identifiers
    and associated details"""

    CR_NAME_LEN = 60

    HEADER_MSG = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
              "*GERRIT BUILD REPORT*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel, crs):
        self.channel = channel
        self.username = "bolt4u"
        self.icon_emoji = ":robot_face:"
        self.crs = crs

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.HEADER_MSG,
                self.DIVIDER_BLOCK,
                *self._get_gerrit_msg(),
            ],
        }

    def _get_gerrit_msg(self):
        msgs = []

        for cr in self.crs:
            #print("Working on CR: \n", cr)


            if 'type' in cr and cr['type'] == 'stats':
                continue

            status = "*BUILD STATUS* \n"
            if 'number' in cr:
                reviewid = '*REVIEW ID*: \n' + str(cr['number'])

            if 'url' in cr:
                url = '*URL*: \n' + str(cr['url'])

            if 'subject' in cr:
                subject = '*SUBJECT*: \n' +  \
                cr['subject'][0:min(self.CR_NAME_LEN, len(cr['subject']))]

            if 'lastUpdated' in cr:
                last_t = cr['lastUpdated']
                last_time = datetime.datetime.fromtimestamp(last_t)
                lastupdated = '*LAST UPDATED*: \n' + str(last_time)

            build_failed = False
            if 'comments' in cr:
                print("Last comment ", cr['comments'][-1])
                if 'message' in cr['comments'][-1]:
                    msg = cr['comments'][-1]['message']
                    print("Message in Last comment: ", msg, '\n')
                    if 'Build' in msg:
                        if 'Failed' in msg:
                            build_failed = True
                            status = status + "FAILED"
                        elif 'Successful' in msg:
                            status = status + "SUCCESSFUL"
                        elif 'Started' in msg:
                            status = status + "RUNNING"

            msg = {
                "type": "section",
                "fields": [
				{
					"type": "mrkdwn",
					"text": reviewid
				},
				{
					"type": "mrkdwn",
					"text": url
				},
				{
					"type": "mrkdwn",
					"text": subject
				},
				{
					"type": "mrkdwn",
					"text": lastupdated
				},
				{
					"type": "mrkdwn",
					"text": status
				},
                ]
            }
            button_msg = {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Retrigger Build"
					},
					"style": "danger",
					"value": "click_me_123"
				},
			]
            }
            msgs.append(msg)
            if build_failed:
              msgs.append(button_msg)
            msgs.append(self.DIVIDER_BLOCK)

        return msgs
