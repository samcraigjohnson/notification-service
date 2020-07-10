import os
import falcon


class NotificationsResource:
    def on_get(self, req, resp):
        resp.media = "Hooray"


class StaticResource:
    def on_get(self, req, resp):
        # do some sanity check on the filename
        resp.status = falcon.HTTP_200
        resp.content_type = "text/html"
        with open(os.path.abspath("./web/html/index.html"), "rb") as f:
            resp.body = f.read()
