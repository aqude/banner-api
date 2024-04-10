CREATE TABLE user_banners (
    id SERIAL PRIMARY KEY,
    tag_ids INTEGER[],
    feature_id INTEGER,
    title TEXT,
    text TEXT,
    url TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    user_token TEXT -- заглушка
);
