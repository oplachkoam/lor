CREATE TABLE IF NOT EXISTS locations
(
    id           UUID PRIMARY KEY,
    character_id UUID        NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    x            FLOAT       NOT NULL,
    y            FLOAT       NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL
);
