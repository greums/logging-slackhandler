from logging import Formatter


class SlackFormatter(Formatter):
    def __init__(self):
        super(SlackFormatter, self).__init__()

    def format(self, record):
        formatted_record = {}
        # if record.levelname == 'INFO':
        #     ret['color'] = 'good'
        # elif record.levelname == 'WARNING':
        #     ret['color'] = 'warning'
        # elif record.levelname == 'ERROR':
        #     ret['color'] = '#E91E63'
        # elif record.levelname == 'CRITICAL':
        #     ret['color'] = 'danger'
        #
        # ret['author_name'] = record.levelname
        # ret['title'] = record.name
        # ret['ts'] = record.created
        # ret['text'] = super(SlackFormatter, self).format(record)
        return formatted_record
