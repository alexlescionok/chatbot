CREATE TABLE IF NOT EXISTS chats (
    id          SERIAL PRIMARY KEY,
    session_id  UUID NOT NULL DEFAULT gen_random_uuid(),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id              SERIAL PRIMARY KEY,
    chat_id         INTEGER NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    role            TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content         TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages(chat_id);