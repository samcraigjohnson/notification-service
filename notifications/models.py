from datetime import datetime
from enum import Enum
from pony import orm

from notifications.db import db


class Events(Enum):
    CREATE = "CREATE"
    EXECUTE = "EXECUTE"
    DELETE = "DELETE"


@orm.db_session
def seed_events():
    for event in Events:
        if not Event.exists(name=event.value):
            Event(name=event.value)


@orm.db_session
def data_setup():
    seed_events()
    u1 = User()
    u2 = User()
    subscribe_user(u1, Events.CREATE)
    subscribe_user(u1, Events.DELETE)
    subscribe_user(u2, Events.EXECUTE)
    subscribe_user(u2, Events.DELETE)

    ts = create_test_scenario()
    execute_test_scenario(ts)
    delete_test_scenario(ts)


@orm.db_session
def execute_test_scenario(ts):
    ts.executed_at = datetime.utcnow()
    create_notification(Events.EXECUTE)


@orm.db_session
def delete_test_scenario(ts):
    ts.deleted_at = datetime.utcnow()
    create_notification(Events.DELETE)


@orm.db_session
def create_test_scenario():
    ts = TestScenario()
    create_notification(Events.CREATE)
    return ts


@orm.db_session
def create_notification(event):
    """ Eventually break this up into a queue """
    db_event = get_event(event)
    notif = Notification(event=db_event)

    # Create a user notification for every subscription
    for sub in db_event.notification_subscriptions:
        UserNotification(user=sub.user, read=False, notification=notif)


@orm.db_session
def subscribe_user(user, event):
    db_event = get_event(event)
    if not NotificationSubscription.exists(user=user, event=db_event):
        return NotificationSubscription(user=user, event=db_event)


@orm.db_session
def get_event(event):
    if event not in Events:
        raise "Unsupported event"

    return Event.get(name=event.value)


class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    notification_subscriptions = orm.Set('NotificationSubscription')
    user_notifications = orm.Set('UserNotification')


class Event(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    notifications = orm.Set('Notification')
    notification_subscriptions = orm.Set('NotificationSubscription')


class TestScenario(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    created_at = orm.Optional(datetime)
    deleted_at = orm.Optional(datetime)
    executed_at = orm.Optional(datetime)

    def before_insert(self):
        self.created_at = datetime.utcnow()


class Notification(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    event = orm.Required(Event)
    user_notifications = orm.Set('UserNotification')
    created_at = orm.Optional(datetime)

    def before_insert(self):
        self.created_at = datetime.utcnow()


class NotificationSubscription(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    user = orm.Required(User)
    event = orm.Required(Event)


class UserNotification(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    user = orm.Required(User)
    read = orm.Required(bool, default=False)
    notification = orm.Required(Notification)
