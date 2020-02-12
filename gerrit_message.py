class GerritMessage:
    """Constructs gerrit message consisting of list of codereview identifiers
    and associated details"""

    HEADER_MSG = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Hi! How is it going? :smile:\n"
                "Let me give you some details on your *CRs*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel, crs):
        self.channel = channel
        self.username = "gerritbot"
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
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "[Replication]: Adding Minio support for replication APIs...\n"
                        "ENG-274249\n"
                        "Build status: failed :white_frowning_face:\n"
                    ),
                },
            },
        ]

