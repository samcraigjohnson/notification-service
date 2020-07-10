--
-- PostgreSQL database schema
--

CREATE TABLE "event" (
  "id" SERIAL PRIMARY KEY,
  "name" TEXT NOT NULL
)

CREATE TABLE "testscenario" (
  "id" SERIAL PRIMARY KEY,
  "created_at" TIMESTAMP,
  "deleted_at" TIMESTAMP,
  "executed_at" TIMESTAMP
)

CREATE TABLE "notification" (
  "id" SERIAL PRIMARY KEY,
  "event" INTEGER NOT NULL,
  "test_scenario" INTEGER NOT NULL,
  "created_at" TIMESTAMP
)

CREATE TABLE "user" (
  "id" SERIAL PRIMARY KEY
)

CREATE TABLE "notificationsubscription" (
  "id" SERIAL PRIMARY KEY,
  "user" INTEGER NOT NULL,
  "event" INTEGER NOT NULL
)


CREATE TABLE "usernotification" (
  "id" SERIAL PRIMARY KEY,
  "user" INTEGER NOT NULL,
  "read" BOOLEAN NOT NULL,
  "notification" INTEGER NOT NULL
)

--
-- Indexes
--

-- We want to quickly get all subscriptions for a given event so this is
-- an important index
CREATE INDEX "idx_notificationsubscription__event" ON "notificationsubscription" ("event")

-- For when we want to get every user notification for a specific notification
CREATE INDEX "idx_usernotification__notification" ON "usernotification" ("notification")

-- Getting all notifications for a user
CREATE INDEX "idx_usernotification__user" ON "usernotification" ("user")

-- Getting all subscriptions for a user
CREATE INDEX "idx_notificationsubscription__user" ON "notificationsubscription" ("user")

-- Getting all notifications for a specific event
CREATE INDEX "idx_notification__event" ON "notification" ("event")

-- Getting all notifications for a test scenario
CREATE INDEX "idx_notification__test_scenario" ON "notification" ("test_scenario")

-- We query a lot for events by name, the event table will most likely
-- always be small extra increase is nice
CREATE INDEX "idx_event_name" ON "event" ("name")

-- For when we are checking if user is already subscribed
CREATE INDEX "idx_notifs_sub_exists" ON "notificationsubscription" ("user", "event")

-- For when we are checking if notification was already sent
CREATE INDEX "idx_user_notifs_exists" ON "usernotification" ("user", "notification")

-- For when we want to filter by read
CREATE INDEX "idx_user_notifs_exists" ON "usernotification" ("read")


--
-- Foreign keys
--
ALTER TABLE "usernotification" ADD CONSTRAINT "fk_usernotification__notification" FOREIGN KEY ("notification") REFERENCES "notification" ("id") ON DELETE CASCADE
ALTER TABLE "usernotification" ADD CONSTRAINT "fk_usernotification__user" FOREIGN KEY ("user") REFERENCES "user" ("id") ON DELETE CASCADE
ALTER TABLE "notificationsubscription" ADD CONSTRAINT "fk_notificationsubscription__event" FOREIGN KEY ("event") REFERENCES "event" ("id") ON DELETE CASCADE
ALTER TABLE "notificationsubscription" ADD CONSTRAINT "fk_notificationsubscription__user" FOREIGN KEY ("user") REFERENCES "user" ("id") ON DELETE CASCADE
ALTER TABLE "notification" ADD CONSTRAINT "fk_notification__event" FOREIGN KEY ("event") REFERENCES "event" ("id") ON DELETE CASCADE
ALTER TABLE "notification" ADD CONSTRAINT "fk_notification__test_scenario" FOREIGN KEY ("test_scenario") REFERENCES "testscenario" ("id") ON DELETE CASCADE
