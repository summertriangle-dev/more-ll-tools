import sqlite3

SCHEMA_INIT = """CREATE TABLE IF NOT EXISTS
state (ordinal INTEGER PRIMARY KEY,
       is_consistent INTEGER,
       card_image TEXT,
       card_idolized_image TEXT,
       round_card_image TEXT,
       round_card_idolized_image TEXT,
       transparent_image TEXT,
       transparent_idolized_image TEXT,
       clean_ur TEXT,
       clean_ur_idolized TEXT)"""

class State(object):
    def __init__(self, arg):
        self.c = sqlite3.connect(arg)
        self.c.row_factory = sqlite3.Row
        self.c.execute(SCHEMA_INIT)

    def ingest_api_object(self, api_object):
        try:
            self.c.execute("""INSERT INTO state VALUES (:id, 0,
                :card_image,
                :card_idolized_image,
                :round_card_image,
                :round_card_idolized_image,
                :transparent_image,
                :transparent_idolized_image,
                :clean_ur,
                :clean_ur_idolized)""", api_object)
        except sqlite3.IntegrityError:
            self.c.execute("""UPDATE state SET
                card_image                 = :card_image,
                card_idolized_image        = :card_idolized_image,
                round_card_image           = :round_card_image,
                round_card_idolized_image  = :round_card_idolized_image,
                transparent_image          = :transparent_image,
                transparent_idolized_image = :transparent_idolized_image,
                clean_ur                   = :clean_ur,
                clean_ur_idolized          = :clean_ur_idolized
                WHERE ordinal = :id""", api_object)

        print("ingest_api_object: {0}".format(api_object["id"]))
        self.c.commit()

    def get_inconsistent_entries(self):
        return self.c.execute("SELECT * FROM state WHERE is_consistent = 0").fetchall()

    def mark_entry_consistent(self, ordinal):
        self.c.execute("UPDATE state SET is_consistent = 1 WHERE ordinal = ?", (ordinal,))
        self.c.commit()

    def extant_ids(self):
        return [k for k, in self.c.execute("SELECT ordinal FROM state").fetchall()]

    def disconnect(self):
        self.c.close()
