# create DB script
import sqlite3 as s

DB_PATH = "warframe.db"
SCHEMA = """
PRAGMA foreign_keys = ON;

-- Primary items table

CREATE TABLE items (
    id INTEGER PRIMARY KEY,

    unique_name TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,

    item_type TEXT NOT NULL, -- prime part, mod, relic, etc
    compat_class TEXT,      -- 

    rarity TEXT,

    is_augment INTEGER,     -- 0/1
    is_prime INTEGER,       -- 0/1

    ducats INTEGER,         -- ducat value

    wiki_url TEXT,
    image_url TEXT
);


-- Drop sources

CREATE TABLE drop_sources (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL  -- vendor, syndicate, enemy, mission, etc
);


-- Direct drops

CREATE TABLE relic_drops (
    id INTEGER PRIMARY KEY,

    item_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,

    chance REAL,
    rarity TEXT,
    drop_type TEXT,
    pool_index INTEGER,

    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (source_id) REFERENCES drop_sources(id),

    UNIQUE (item_id, source_id, drop_type)
);


-- Relics

CREATE TABLE relic_rewards (
    id INTEGER PRIMARY KEY,

    relic_id INTEGER NOT NULL,
    reward_item_id INTEGER NOT NULL,

    rarity TEXT NOT NULL,
    
    FOREIGN KEY (relic_id) REFERENCES items(id),
    FOREIGN KEY (reward_item_id) REFERENCES items(id),

    UNIQUE (relic_id, reward_item_id)
);


-- Trade price snapshot

CREATE TABLE item_trade_prices (
    item_id INTEGER PRIMARY KEY,

    cheapest_listing INTEGER,
    avg_recent REAL,
    volume INTEGER,
    average REAL,
    ten_day_average REAL,

    last_updated TEXT,

    FOREIGN KEY (item_id) REFERENCES items(id)
);
"""

def create_db(path: str = DB_PATH) -> s.Connection:
    conn = s.connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn

if __name__ == "__main__":
    conn = create_db()
    conn.close()
    print(f"Database created at '{DB_PATH}'")
