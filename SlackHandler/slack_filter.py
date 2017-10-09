from logging import Filter


class SlackFilter(Filter):
    def filter(self, record):
        return getattr(record, 'notify_slack', False)
