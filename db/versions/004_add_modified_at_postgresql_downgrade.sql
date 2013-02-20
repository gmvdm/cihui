BEGIN;

ALTER TABLE list
      DROP COLUMN modified_at;

COMMIT;
