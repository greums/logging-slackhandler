from logging import Handler, Formatter
from requests_futures.sessions import FuturesSession
from SlackLogger.version import get_version

__version__ = get_version()

LEVEL_TO_COLOR = {
    'DEBUG': '#e3e4e6',
    'INFO': '#4183c4',
    'WARNING': '#daa038',
    'ERROR': '#d9534f',
    'CRITICAL': '#2c2d30'
}


class SlackHandler(Handler):
    def __init__(self, webhook_url, username=None, channel=None, icon_emoji=':snake:'):
        super(SlackHandler, self).__init__()

        self.webhook_url = webhook_url
        self.username = username
        self.channel = channel
        self.icon_emoji = icon_emoji

        self.session = FuturesSession()

    def emit(self, record):
        if isinstance(self.formatter, SlackFormatter):
            attachment = self.format(record)
        else:
            attachment = {'text': self.format(record)}

        payload = {
            'channel': self.channel,
            'icon_emoji': self.icon_emoji,
            'username': self.username,
            'attachments': [
                attachment
            ]
        }

        self.session.post(self.webhook_url, json=payload)


class SlackFormatter(Formatter):
    # def __init__(self):
    #     super(SlackFormatter, self).__init__()

    def format(self, record):
        return {
            'author_name': record.levelname,
            'color': LEVEL_TO_COLOR[record.levelname],
            'mrkdwn': True,
            'text': super(SlackFormatter, self).format(record),
            'title': record.name,
            'ts': record.created
        }
