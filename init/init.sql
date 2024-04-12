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
    user_token TEXT DEFAULT '9e4328cad64f4e51aef1dbc6322db313' -- заглушка
);

INSERT INTO user_banners
    (tag_ids, feature_id, title, text, url, is_active, created_at, updated_at, user_token)
VALUES
    (1, [10, 11], 'Заголовок', 'Текст', 'https://google.com', true, now(), now(), '9e4328cad64f4e51aef1dbc6322db313'),
    (2, [2], 'Заголовок', 'Текст', 'https://yandex.ru', true, now(), now(), '9e4328cad64f4e51aef1dbc6322db313'),
    (3, [3], 'Заголовок', 'Текст', 'https://vk.com', true, now(), now(), '9e4328cad64f4e51aef1dbc6322db313')