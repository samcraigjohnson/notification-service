import os
import falcon
import logging

from pony import orm

# Setup environment variables
from dotenv import load_dotenv
if os.environ.get("ENIVORMENT", "") == "prod":
    load_dotenv(dotenv_path=".prod.env")
elif os.environ.get("TEST", "") == "true":
    load_dotenv(dotenv_path=".test.env")
else:
    load_dotenv(verbose=True)

from notifications import db
if os.environ.get("SQL_DEBUG", "") == "true":
    orm.sql_debug(True)

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
static = controllers.StaticResource()

app.add_route("/api/cards", notifs)
app.add_route("/", static)
