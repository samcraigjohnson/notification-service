CREATE INDEX "idx_event_name" ON "event" ("name")
CREATE INDEX "idx_notifs_sub_exists" ON "notificationsubscription" ("user", "event")
