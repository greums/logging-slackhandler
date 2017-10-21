"""
This module provides additionals handler, formatter and filter for the logging
package, so you can send Python log records to a Slack Incoming Webhook.
"""
import atexit
import json
from logging import getLogger, Handler, Formatter, Filter
from multiprocessing import cpu_count
from threading import Thread
from SlackLogger.version import get_version

try:
    from urllib2 import urlopen
    from Queue import Queue
except ImportError:
    from urllib.request import urlopen
    from queue import Queue

__version__ = get_version()
logger = getLogger(__name__)


class Worker(Thread):
    """
    Thread executing tasks from a given tasks queue.
    """
    def __init__(self, tasks):
        super(Worker, self).__init__()

        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as error:
                logger.error('Failed to process task: %s', str(error))
            finally:
                self.tasks.task_done()


class WorkerPool(object):
    """
    Pool of threads consuming tasks from a queue.

    :param num_threads: number of concurrent workers to create in pool.
    """
    def __init__(self, num_threads):
        self.tasks_queue = Queue()

        for _ in range(num_threads):
            Worker(self.tasks_queue)

    def add_task(self, func, *args, **kwargs):
        """Add a task to the queue"""
        self.tasks_queue.put((func, args, kwargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks_queue.join()


class SlackHandler(Handler):
    """
    SlackHandler instances dispatch logging events to Slack Incoming Webhook.

    :param webhook_url: Slack Incoming Webhook URL.
    :param username: (optional) message sender username.
    :param channel: (optional) Slack channel to post to.
    :param icon_emoji: (optional) customize emoji for message sender.
    :param timeout: (optional) specifies a timeout in seconds for blocking operations.
    :param pool_size: (optional) specifies number of workers processing records queue.
    """
    def __init__(self, webhook_url, username=None, channel=None, icon_emoji=':snake:', timeout=10, pool_size=cpu_count()):
        super(SlackHandler, self).__init__()

        self.url = webhook_url
        self.username = username
        self.channel = channel
        self.icon_emoji = icon_emoji
        self.timeout = timeout

        self.setFormatter(SlackFormatter())

        self.workers = WorkerPool(pool_size)
        atexit.register(self.workers.wait_completion)

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

        data = json.dumps(payload).encode('utf-8')
        self.workers.add_task(urlopen, self.url, data, timeout=self.timeout)


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
