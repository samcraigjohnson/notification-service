CREATE INDEX "idx_event_name" ON "event" ("name")

-- For when we are checking if user is already subscribed
CREATE INDEX "idx_notifs_sub_exists" ON "notificationsubscription" ("user", "event")

-- For when we are checking if notification was already sent
CREATE INDEX "idx_user_notifs_exists" ON "usernotification" ("user", "notifica


-- For when we want to filter by read
CREATE INDEX "idx_user_notifs_exists" ON "usernotification" ("read")
