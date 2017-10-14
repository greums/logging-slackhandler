"""
This module provides additionals handler, formatter and filter for the logging
package, so you can send Python log records to a Slack Incoming Webhook.
"""
from logging import Handler, Formatter, Filter
from requests_futures.sessions import FuturesSession
from SlackLogger.version import get_version

__version__ = get_version()


class SlackHandler(Handler):
    """
    SlackHandler instances dispatch logging events to Slack Incoming Webhook.

    :param webhook_url: Slack Incoming Webhook URL.
    :param username: (optional) Message sender username.
    :param channel: (optional) Slack channel to post to.
    :param icon_emoji: (optional) Customize emoji for message sender.
    """
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
    """
    SlackFormatter instances format log record and return a dictionary that can
    be sent as a Slack message attachment.
    """
    def __init__(self):
        super(SlackFormatter, self).__init__()

        self.level_to_color = {
            'DEBUG':    '#AC92EC',
            'INFO':     '#48CFAD',
            'WARNING':  '#FFCE54',
            'ERROR':    '#FC6E51',
            'CRITICAL': '#DA4453'
        }

    def format(self, record):
        return {
            'author_name': record.levelname,
            'color': self.level_to_color[record.levelname],
            'mrkdwn_in': ['text'],
            'text': super(SlackFormatter, self).format(record),
            'title': record.name,
            'ts': record.created
        }


class SlackFilter(Filter):
    """
    SlackFilter instances can be use to determine if the specified record is to
    be sent to Slack Incoming Webhook.

    :param allow: filtering rule for log record.
    """
    def __init__(self, allow=False):
        super(SlackFilter, self).__init__()

        self.allow = allow

    def filter(self, record):
        return getattr(record, 'slack', self.allow)
