from pony import orm

from notifications import models

from . import Worker
from .user_notifications import UserNotificationWorker


class NotificationWorker(Worker):
    def __init__(self, event=None):
        self.args = event.value

    @orm.db_session
    def process(self):
        event = models.Events[self.args]
        db_event = models.get_event(event)
        notif = models.Notification(event=db_event)

        # Make sure notification is created before user notifications
        orm.commit()

        # Create a user notification for every subscription
        # Push it into a separate worker in case we want to
        # email them/etc
        for sub in db_event.notification_subscriptions:
            UserNotificationWorker(user_id=sub.user.id,
                                   notification_id=notif.id).enqueue()
