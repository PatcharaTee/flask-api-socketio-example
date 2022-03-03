DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS room;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL,
    locked BOOLEAN,
    password TEXT,
    FOREIGN KEY (owner_id) REFERENCES user (id)
)