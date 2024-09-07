CREATE TABLE guests (
    email TEXT NOT NULL,
    firstname TEXT NOT NULL,
    invite TEXT NOT NULL,  -- CEREMONY or EVENING
    lastname TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    rsvp INTEGER DEFAULT 0,  -- Boolean (1 or 0)
);