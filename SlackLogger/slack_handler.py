from logging import Handler

from requests_futures.sessions import FuturesSession

level_to_color = {
    'DEBUG': '#00bfff',
    'INFO': '#40ff00',
    'WARNING': '#ffff00',
    'ERROR': '#ff8000',
    'CRITICAL': '#ff0000'
}
session = FuturesSession()


class SlackHandler(Handler):

    def __init__(self, webhook_url, username=None, channel=None, icon_emoji=':snake:'):
        super(SlackHandler, self).__init__()

        self.webhook_url = webhook_url
        self.username = username
        self.channel = channel
        self.icon_emoji = icon_emoji

    def emit(self, record):
        payload = {
            'channel': self.channel,
            'icon_emoji': self.icon_emoji,
            'username': self.username,
            'attachments': [{
                'color': level_to_color[record.levelname],
                'title': record.name,
                'text': self.format(record),
                'pretext': record.levelname
            }]
        }

        session.post(self.webhook_url, json=payload)
