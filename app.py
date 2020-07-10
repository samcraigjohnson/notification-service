import os
import falcon
import logging

from pony import orm
orm.sql_debug(True)

# Setup environment variables
from dotenv import load_dotenv
if os.environ.get("ENIVORMENT", "") == "prod":
    load_dotenv(dotenv_path=".prod.env")
elif os.environ.get("TEST", "") == "true":
    load_dotenv(dotenv_path=".test.env")
else:
    load_dotenv(verbose=True)

from notifications import db
logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))

from notifications import models
from notifications import controllers

db.db.generate_mapping(create_tables=True)

app = application = falcon.API()

###
# Config
###

app.resp_options.secure_cookies_by_default = False

###
# Routes
###

app.add_static_route("/bin", os.path.abspath("./web/bin"))
app.add_static_route("/css", os.path.abspath("./web/css"))

notifs = controllers.NotificationsResource()
ts = controllers.TestScenarioResource()
static = controllers.StaticResource()

app.add_route("/api/notifs", notifs)
app.add_route("/api/notifs/subs", notifs, suffix="subs")
app.add_route("/api/notifs/{notif_id:int}/read", notifs, suffix="read")

app.add_route("/api/ts", ts)
app.add_route("/api/ts/{test_id:int}", ts, suffix="single")
app.add_route("/api/ts/{test_id:int}/execute", ts, suffix="execute")
app.add_route("/", static)

###
# Setup
###

models.data_setup()
