from pony import orm

from notifications import models

from . import Worker


class UserNotificationWorker(Worker):
    def __init__(self, user_id=None, notification_id=None):
        self.args = {'user_id': user_id, 'notification_id': notification_id}

    @orm.db_session
    def process(self):
        user = models.User[self.args['user_id']]
        notif = models.Notification[self.args['notification_id']]

        # In case message gets read twice
        if not models.UserNotification.exists(user=user, notification=notif):
            models.UserNotification(user=user, notification=notif, read=False)
