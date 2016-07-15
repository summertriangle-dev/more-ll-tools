#!/usr/bin/env python3
# detable: Encrypted sqlite3 fixer-upper

# The Holy Constituency of the Summer Triangle, 2016.
# No rights reserved; see readme for more information.
import sys
import sqlite3
import json
import pyaes
import base64

QUERY_TO_FIND_ENCRYPTED_TABLES = """
SELECT name FROM sqlite_master WHERE `type` = 'table'
AND sql GLOB '*_encryption_release_id*'
AND sql GLOB '*release_tag*'"""

QUERY_TO_FIND_ENCRYPTED_ROWS = """
SELECT rowid, release_tag, _encryption_release_id FROM `{0}`
WHERE _encryption_release_id NOT NULL
"""

QUERY_TO_REPLACE_ENCRYPTED_COLUMNS = "UPDATE `{1}` SET {0} WHERE rowid = :__rowid"

def decrypt_this(enc, keyid):
    use = G_KEYBAG.get(str(keyid))["key"]
    if use is None:
        raise RuntimeError("no key for keyid {0}".format(keyid))

    ciphertext = base64.b64decode(enc.encode("ascii"))
    aes_ctx = pyaes.AESModeOfOperationCBC(base64.b64decode(use.encode("ascii")),
        iv=ciphertext[:16])
    ciphertext = ciphertext[16:]
    plaintext = []

    while ciphertext:
        blk = ciphertext[:16]
        plaintext.append(aes_ctx.decrypt(blk))
        ciphertext = ciphertext[16:]

    json_ = b"".join(plaintext)
    pad = json_[-1]
    json_ = json_[:-pad]

    overlay = json.loads(json_.decode("utf8"))
    return overlay

def decrypt_rows(handle, in_table):
    rows = handle.execute(QUERY_TO_FIND_ENCRYPTED_ROWS.format(in_table)).fetchall()
    if rows is None:
        return

    for rowid, enc_values, keyid in rows:
        try:
            dec_values = decrypt_this(enc_values, keyid)
        except RuntimeError as e:
            print("error for rowid", rowid, "of", in_table, ":", str(e))
            continue

        dec_values["_encryption_release_id"] = None
        dec_values["release_tag"] = None
        clause = ", ".join("`{0}` = :{0}".format(key) for key in dec_values)

        dec_values["__rowid"] = rowid
        dec_values["__table"] = in_table
        handle.execute(QUERY_TO_REPLACE_ENCRYPTED_COLUMNS.format(clause, in_table), dec_values)

    print(in_table, ": will update", len(rows), "rows")

def main(db_path: "DB file to operate on (in-place, be careful)",
         keybag_path: """JSON file containing keys, schema: {"<KEYID>": {"key": "<BASE64 KEY MATERIAL>"}} """):
    global G_KEYBAG
    with open(keybag_path, "r") as f:
        G_KEYBAG = json.load(f)

    db = sqlite3.connect(db_path)
    for tablename, in db.execute(QUERY_TO_FIND_ENCRYPTED_TABLES):
        decrypt_rows(db, tablename)
    db.commit()
    db.close()

if __name__ == '__main__':
    import plac
    plac.call(main)
