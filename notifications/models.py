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

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class TestScenario(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    notifications = orm.Set("Notification")
    created_at = orm.Optional(datetime)
    deleted_at = orm.Optional(datetime)
    executed_at = orm.Optional(datetime)

    def before_insert(self):
        self.created_at = datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'created_at': str(self.created_at),
            'executed_at': str(self.executed_at),
            'deleted_at': str(self.deleted_at),
        }


class Notification(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    event = orm.Required(Event)
    test_scenario = orm.Required(TestScenario)
    user_notifications = orm.Set('UserNotification')
    created_at = orm.Optional(datetime)

    def before_insert(self):
        self.created_at = datetime.utcnow()

    def message(self):
        if self.event.name == Events.CREATE.value:
            return f"Test scenario was created at {self.test_scenario.created_at}"

        if self.event.name == Events.EXECUTE.value:
            return f"Test scenario was executed at {self.test_scenario.executed_at}"

        if self.event.name == Events.DELETE.value:
            return f"Test scenario was deleted at {self.test_scenario.deleted_at}"


class NotificationSubscription(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    user = orm.Required(User)
    event = orm.Required(Event)

    def to_json(self):
        data = self.to_dict()
        data['event'] = self.event.to_json()
        return data


class UserNotification(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    user = orm.Required(User)
    read = orm.Required(bool, default=False)
    notification = orm.Required(Notification)

    def to_json(self):
        data = self.to_dict()
        data['type'] = self.notification.event.name
        data['notification'] = self.notification.message()
        return data
