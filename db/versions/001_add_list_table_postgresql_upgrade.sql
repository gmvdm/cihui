BEGIN;

CREATE TABLE list (
       id SERIAL PRIMARY KEY,
       title TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT NOW()
);

COMMIT;