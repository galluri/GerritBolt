class GerritMessage:
    """Constructs gerrit message consisting of list of codereview identifiers
    and associated details"""

    CR_NAME_LEN = 60

    HEADER_MSG = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Hi! How is it going? :smile:\n"
                "Let me help you with some of your *codereviews*"
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
                self.DIVIDER_BLOCK,
            ],
        }

    def _get_gerrit_msg(self):
        #return [
        #    {
        #        "type": "section",
        #        "text": {
        #            "type": "mrkdwn",
        #            "text": (
        #                "[Replication]: Adding Minio support for replication APIs...\n"
        #                "ENG-274249\n"
        #                "Build status: failed :white_frowning_face:\n"
        #            ),
        #        },
        #    },
        #]
        msgs = []
        for cr in crs:
            print("Working on CR: %s\n", cr)

            text = ""
            if 'number' in cr:
                text = text + '_Number_: ' + cr['number'] + '\n'

            if 'subject' in cr:
                text = text + '_Subject_: ' +  \
                cr['subject'][0:min(CR_NAME_LEN, len(cr['subject']))] + '\n'

            if 'lastUpdated' in cr:
                text = text + '_LastUpdated_: ' + cr['lastUpdated'] + '\n'

            if 'comments' in cr:
               if 'Build' in cr['comments'][-1]:
                if 'Failed' in cr['comments'][-1]:
                    text = text + "_Build Status_: Failed"
                else if 'Successful' in cr['comments'][-1]:
                    text = text + "_Build Status_: Successful"
                else if 'Started' in cr['comments'][-1]:
                    text = txxt + "_Build Status_: Running"

            msg = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text,
                },
            }
            msgs.append(msg)
            msgs.append(DIVIDER_BLOCK)

        return msgs
