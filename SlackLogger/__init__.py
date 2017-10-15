"""
This module provides additionals handler, formatter and filter for the logging
package, so you can send Python log records to a Slack Incoming Webhook.
"""
import json
from logging import Handler, Formatter, Filter
from threading import Thread
from SlackLogger.version import get_version
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

__version__ = get_version()


class ThreadedRequest(Thread):
    """
    ThreadedRequest instances send message to message to Slack Incoming Webhook
    without blocking following log record.

    :param url: Slack Incoming Webhook URL.
    :param payload: message to be sent to Slack Webhook.
    :param timeout: (optional) specifies a timeout in seconds for operations.

    """
    def __init__(self, url, payload, timeout=10):
        super(ThreadedRequest, self).__init__()

        self.url = url
        self.data = json.dumps(payload).encode('utf-8')
        self.timeout = timeout

    def run(self):
        urlopen(self.url, self.data, timeout=self.timeout)


class SlackHandler(Handler):
    """
    SlackHandler instances dispatch logging events to Slack Incoming Webhook.

    :param webhook_url: Slack Incoming Webhook URL.
    :param username: (optional) message sender username.
    :param channel: (optional) Slack channel to post to.
    :param icon_emoji: (optional) customize emoji for message sender.
    """
    def __init__(self, webhook_url, username=None, channel=None, icon_emoji=':snake:'):
        super(SlackHandler, self).__init__()

        self.webhook_url = webhook_url
        self.username = username
        self.channel = channel
        self.icon_emoji = icon_emoji

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

        ThreadedRequest(self.webhook_url, payload).start()


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
