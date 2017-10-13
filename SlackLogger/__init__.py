from logging import Handler, Formatter
from requests_futures.sessions import FuturesSession
from SlackLogger.version import get_version

__version__ = get_version()

LEVEL_TO_COLOR = {
    'DEBUG': '#AC92EC',
    'INFO': '#48CFAD',
    'WARNING': '#FFCE54',
    'ERROR': '#FC6E51',
    'CRITICAL': '#DA4453'
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
    def format(self, record):
        return {
            'author_name': record.levelname,
            'color': LEVEL_TO_COLOR[record.levelname],
            'mrkdwn_in': ['text'],
            'text': super(SlackFormatter, self).format(record),
            'title': record.name,
            'ts': record.created
        }
