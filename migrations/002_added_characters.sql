CREATE TABLE IF NOT EXISTS characters
(
    id          UUID PRIMARY KEY,
    name        TEXT        NOT NULL UNIQUE,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL
);
