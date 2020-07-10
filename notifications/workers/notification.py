from pony import orm

from . import Worker


class NotificationWorker(Worker):
    def __init__(self):
        pass

    @orm.db_session
    def process(self):
        pass
