from datetime import datetime
from pony import orm

from notifications.db import db


@orm.db_session
def seed_data():
    u1 = User()
    u2 = User()

    ts = TestScenario()

    e1 = Event(type="created")
    e2 = Event(type="executed")
    e3 = Event(type="deleted")


class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)


class Event(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    notifications = orm.Set('Notification')


class TestScenario(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    notifications = orm.Set('Notification')
    created_at = orm.Optional(datetime)
    deleted_at = orm.Optional(datetime)
    executed_at = orm.Optional(datetime)

    def before_insert(self):
        self.created_at = datetime.utcnow()


class Notification(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    event = orm.Required(Event)
    test_scenario = orm.Required(TestScenario)
    created_at = orm.Optional(datetime)

    def before_insert(self):
        self.created_at = datetime.utcnow()

    # time
    # ts


class NotificationSubscription(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    # user
    # event
    type = orm.Required(str)


class UserNotification(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    # user
    # read
