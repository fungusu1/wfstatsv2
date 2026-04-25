# create DB script
import sqlite3 as s

DB_PATH = "warframe.db"
SCHEMA = """
PRAGMA foreign_keys = ON;

-- =========================
-- Core items
-- =========================

CREATE TABLE items (
    id INTEGER PRIMARY KEY,

    unique_name TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,

    type TEXT,              -- e.g. "Warframe Mod"
    compat_class TEXT,      -- e.g. "Trinity", "Shotgun"

    category TEXT,          -- e.g. "Mods"
    rarity TEXT,

    is_augment INTEGER,     -- 0/1
    tradable INTEGER,       -- 0/1
    is_prime INTEGER,       -- 0/1
    transmutable INTEGER,   -- 0/1
    masterable INTEGER,     -- 0/1

    ducats INTEGER,         -- intrinsic sell value (if present)

    release_date TEXT,

    wiki_available INTEGER,
    wiki_url TEXT,
    image_name TEXT
);

-- =========================
-- Drop sources
-- =========================

CREATE TABLE drop_sources (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- =========================
-- Item drops (junction)
-- =========================

CREATE TABLE item_drops (
    id INTEGER PRIMARY KEY,

    item_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,

    drop_type TEXT,     -- raw from JSON
    chance REAL,
    rarity TEXT,

    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (source_id) REFERENCES drop_sources(id),

    UNIQUE (item_id, source_id, drop_type)
);

-- =========================
-- Trade price snapshot
-- =========================

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
