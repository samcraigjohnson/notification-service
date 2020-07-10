--
-- PostgreSQL database schema
--

CREATE TABLE "event" (
  "id" SERIAL PRIMARY KEY,
  "name" TEXT NOT NULL
)

CREATE TABLE "notification" (
  "id" SERIAL PRIMARY KEY,
  "event" INTEGER NOT NULL,
  "created_at" TIMESTAMP
)

CREATE INDEX "idx_notification__event" ON "notification" ("event")

ALTER TABLE "notification" ADD CONSTRAINT "fk_notification__event" FOREIGN KEY ("event") REFERENCES "event" ("id") ON DELETE CASCADE

CREATE TABLE "testscenario" (
  "id" SERIAL PRIMARY KEY,
  "created_at" TIMESTAMP,
  "deleted_at" TIMESTAMP,
  "executed_at" TIMESTAMP
)

CREATE TABLE "user" (
  "id" SERIAL PRIMARY KEY
)

CREATE TABLE "notificationsubscription" (
  "id" SERIAL PRIMARY KEY,
  "user" INTEGER NOT NULL,
  "event" INTEGER NOT NULL
)

CREATE INDEX "idx_notificationsubscription__event" ON "notificationsubscription" ("event")

CREATE INDEX "idx_notificationsubscription__user" ON "notificationsubscription" ("user")

ALTER TABLE "notificationsubscription" ADD CONSTRAINT "fk_notificationsubscription__event" FOREIGN KEY ("event") REFERENCES "event" ("id") ON DELETE CASCADE
ALTER TABLE "notificationsubscription" ADD CONSTRAINT "fk_notificationsubscription__user" FOREIGN KEY ("user") REFERENCES "user" ("id") ON DELETE CASCADE

CREATE TABLE "usernotification" (
  "id" SERIAL PRIMARY KEY,
  "user" INTEGER NOT NULL,
  "read" BOOLEAN NOT NULL,
  "notification" INTEGER NOT NULL
)

CREATE INDEX "idx_usernotification__notification" ON "usernotification" ("notification")
CREATE INDEX "idx_usernotification__user" ON "usernotification" ("user")

ALTER TABLE "usernotification" ADD CONSTRAINT "fk_usernotification__notification" FOREIGN KEY ("notification") REFERENCES "notification" ("id") ON DELETE CASCADE
ALTER TABLE "usernotification" ADD CONSTRAINT "fk_usernotification__user" FOREIGN KEY ("user") REFERENCES "user" ("id") ON DELETE CASCADE
