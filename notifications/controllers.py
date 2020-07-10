import os
import falcon
from pony import orm

from notifications import models
from notifications.workers.notification import NotificationWorker


class NotificationsResource:
    @orm.db_session
    def on_get(self, req, resp):
        resp.media = [un.to_json() for un in models.UserNotification.select()]

    def on_post_read(self, req, resp, notif_id):
        models.UserNotification[notif_id].read = True


class TestScenarioResource:
    @orm.db_session
    def on_get(self, req, resp):
        resp.media = [ts.to_json() for ts in models.TestScenario]

    @orm.db_session
    def on_post(self, req, resp):
        ts = models.create_test_scenario()
        orm.commit()

        NotificationWorker(event=models.Events.CREATE, test_id=ts.id).enqueue()
        resp.media = ts.to_json()

    def on_post_execute(self, req, resp, test_id):
        models.execute_test_scenario(test_id)
        NotificationWorker(event=models.Events.EXECUTE,
                           test_id=test_id).enqueue()

    def on_delete_single(self, req, resp, test_id):
        models.delete_test_scenario(test_id)
        NotificationWorker(event=models.Events.DELETE,
                           test_id=test_id).enqueue()


class StaticResource:
    def on_get(self, req, resp):
        # do some sanity check on the filename
        resp.status = falcon.HTTP_200
        resp.content_type = "text/html"
        with open(os.path.abspath("./web/html/index.html"), "rb") as f:
            resp.body = f.read()
