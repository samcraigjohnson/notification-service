from pony import orm

import os

db = orm.Database()
db.bind(
    provider="postgres",
    user=os.environ["PG_USER"],
    password=os.environ["PG_PWD"],
    host=os.environ["PG_HOST"],
    database=os.environ["PG_DB"],
)
