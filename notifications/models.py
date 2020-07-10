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
    """ Create some seed data to test """
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
def execute_test_scenario(ts_id):
    TestScenario[ts_id].executed_at = datetime.utcnow()


@orm.db_session
def delete_test_scenario(ts_id):
    TestScenario[ts_id].deleted_at = datetime.utcnow()


@orm.db_session
def create_test_scenario():
    ts = TestScenario()
    return ts


@orm.db_session
def subscribe_user(user, event):
    """ Subscribe a user to a type of event, only allow
    one subscription per user per event
    """
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
