CREATE TABLE guests (
    email TEXT NOT NULL,
    firstname TEXT NOT NULL,
    invite TEXT NOT NULL,  -- CEREMONY or EVENING
    lastname TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    rsvp TEXT NULL,
    diet TEXT NULL
);