import sqlite3
import datetime
import json
from collections import namedtuple
import code

# basically libcard-lite, with the advantage that it's not 3 years old

SMILE    = 1
PURE     = 2
COOL     = 3
ALL      = 5

N   = 1
R   = 2
SR  = 3
UR  = 4
SSR = 5

TIMED        = 1
HITS         = 3
COMBO        = 4
POINTS       = 5
PERFECTS     = 6
PERFECT_STAR = 12

SKILL_RAISE     = 0
SMALL_LOCK      = 4
BIG_LOCK        = 5
STAMINA_RESTORE = 9
SCORE_UP        = 11

RARITIES_STRING = {
    N: "N",
    R: "R",
    SR: "SR",
    SSR: "SSR",
    UR: "UR",
}

ATTRIBUTES_STRING = {
    PURE: "Pure",
    SMILE: "Smile",
    COOL: "Cool",
    ALL: "All",
}

EFFECT_BASED_SKILL_NAMES = {
    SCORE_UP: "Score Up",
    STAMINA_RESTORE: "Healer",
    BIG_LOCK: "Perfect Lock",
    SMALL_LOCK: "Perfect Lock",
    SKILL_RAISE: "Special",
}

def describe_skill_proc_req(trigger_type):
    if trigger_type == TIMED:
        return "Every {skill[trigger_value]} seconds,"
    elif trigger_type == HITS:
        return "For every {skill[trigger_value]} notes,"
    elif trigger_type == COMBO:
        return "For every {skill[trigger_value]} hit combo string,"
    elif trigger_type == POINTS:
        return "For every {skill[trigger_value]} points scored,"
    elif trigger_type == PERFECTS:
        return "For every {skill[trigger_value]} perfects,"
    elif trigger_type == PERFECT_STAR:
        return "For every perfect on a starred note,"

    raise Exception("???" + str(trigger_type))

def describe_skill_effect(effect_type):
    if effect_type == SMALL_LOCK:
        return "there is a {skill[activation_rate]}% chance of turning all greats in the next {rounded_dsc_time} seconds into perfects."
    elif effect_type == BIG_LOCK:
        return "there is a {skill[activation_rate]}% chance of turning all goods and greats in the next {rounded_dsc_time} seconds into perfects."
    elif effect_type == STAMINA_RESTORE:
        return "there is a {skill[activation_rate]}% chance of recovering players HP by {skill[effect_value]:.0f}."
    elif effect_type == SCORE_UP:
        return "there is a {skill[activation_rate]}% chance of increasing players score by {skill[effect_value]:.0f} points."

    raise Exception("???" + str(effect_type))

SHARED_SKILL_NAMES = {
    6: "Perfect Charm",
    4: "Rhythmical Charm",
    7: "Timer Yell",
    1: "Timer Charm",
    10: "Rhythmical Yell",
    3: "Total Charm",
    15: "Total Trick",
    12: "Perfect Yell",
    9: "Total Yell",
    13: "Timer Trick",
}

class UnitDB(object):
    light_skill_t = namedtuple("light_skill_t", ("id", "name", "type_name", "description"))

    def __init__(self, arg, namelist):
        self.c = sqlite3.connect(arg)
        self.c.row_factory = sqlite3.Row

        with open(namelist, "r") as nlf:
            self.names = json.load(nlf)

    def get_valid_card_numbers(self):
        return [k for k, in self.c.execute("SELECT unit_number FROM unit_m WHERE _encryption_release_id IS NULL AND unit_number < 10001").fetchall()]

    def fetch_skill_parameters(self, skill_id):
        row = self.c.execute("SELECT * FROM unit_skill_m LEFT JOIN unit_skill_level_m "
            "WHERE unit_skill_m.unit_skill_id = ? AND unit_skill_level_m.unit_skill_id = ? "
            "AND skill_level = 1 LIMIT 1", (skill_id, skill_id)).fetchone()

        def description(skt):
            if skt["skill_effect_type"] == SKILL_RAISE:
                return "Used to level skills for cards of the same attribute"

            f = skt["discharge_time"]
            if f - int(f) <= 0.001:
                f = int(f)

            return " ".join((
                describe_skill_proc_req(skt["trigger_type"]),
                describe_skill_effect(skt["skill_effect_type"])
            )).format(skill=skt, rounded_dsc_time=f) + " (Level 1)"

        struct = self.light_skill_t(
            row["unit_skill_id"],
            row["name"],
            SHARED_SKILL_NAMES.get(row["unit_skill_id"], EFFECT_BASED_SKILL_NAMES.get(row["skill_effect_type"])),
            description(row),
        )

        return struct

    def fetch_lskill_name(self, skill_id):
        row = self.c.execute("SELECT name FROM unit_leader_skill_m WHERE unit_leader_skill_id = ?", (skill_id,)).fetchone()

        D = {
            "ス": "\x04Smile",
            "ピ": "\x03Pure",
            "ク": "\x03Cool",
        }

        S = {
            "パワー": "Power",
            "ハート": "Heart",
            "プリンセス": "Princess",

            "エンジェル": "Angel",
            "エンプレス": "Empress",
            "スター": "Star",
        }

        discriminator = D[row["name"][0]]
        prefix = discriminator[1:]
        rest = row["name"][ord(discriminator[0]):]
        suffix = S[rest]

        return " ".join((prefix, suffix))

    def skt_card_struct(self, ordinal):
        card = self.c.execute("SELECT * FROM unit_m WHERE unit_number = ?", (ordinal,)).fetchone()

        c = {}
        c["game_id"] = card["unit_id"]
        c["attribute"] = ATTRIBUTES_STRING.get(card["attribute_id"])
        c["rarity"]  = RARITIES_STRING.get(card["rarity"])
        c["id"] = card["unit_number"]
        c["hp"] = max(card["hp_max"] - 1, 1)
        c["release_date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        c["is_special"] = bool(card["disable_rank_up"])
        c["is_promo"] = card["normal_icon_asset"] == card["rank_max_icon_asset"] and not c["is_special"]

        c["name"] = self.names[card["name"]]
        c["idol"] = self.names[card["name"]]

        k = self.c.execute("SELECT * FROM unit_level_up_pattern_m WHERE unit_level_up_pattern_id = ? AND "
            "(unit_level = 1 OR unit_level = ?) ORDER BY unit_level",
            (card["unit_level_up_pattern_id"], card["before_level_max"]))

        level1 = k.fetchone()
        levelpreimax = k.fetchone() or level1

        c["minimum_statistics_smile"] = card["smile_max"] - level1["smile_diff"]
        c["minimum_statistics_pure"]  = card["pure_max"] - level1["pure_diff"]
        c["minimum_statistics_cool"]  = card["cool_max"] - level1["cool_diff"]

        c["non_idolized_maximum_statistics_smile"] = card["smile_max"] - levelpreimax["smile_diff"]
        c["non_idolized_maximum_statistics_pure"] =  card["pure_max"] - levelpreimax["pure_diff"]
        c["non_idolized_maximum_statistics_cool"] =  card["cool_max"] - levelpreimax["cool_diff"]

        c["idolized_maximum_statistics_smile"] = card["smile_max"]
        c["idolized_maximum_statistics_pure"] =  card["pure_max"]
        c["idolized_maximum_statistics_cool"] =  card["cool_max"]

        if c["is_promo"] or c["rarity"] == RARITIES_STRING[N]:
            c["non_idolized_maximum_statistics_smile"] = 0
            c["non_idolized_maximum_statistics_pure"] = 0
            c["non_idolized_maximum_statistics_cool"] = 0

        if c["is_special"]:
            c["hp"] = 0
            c["minimum_statistics_smile"] = 0
            c["minimum_statistics_pure"]  = 0
            c["minimum_statistics_cool"]  = 0
            c["non_idolized_maximum_statistics_smile"] = 0
            c["non_idolized_maximum_statistics_pure"] =  0
            c["non_idolized_maximum_statistics_cool"] =  0
            c["idolized_maximum_statistics_smile"] = 0
            c["idolized_maximum_statistics_pure"] =  0
            c["idolized_maximum_statistics_cool"] =  0

        if card["default_unit_skill_id"]:
            sk = self.fetch_skill_parameters(card["default_unit_skill_id"])
            c["skill"] = sk.type_name
            c["skill_details"] = sk.description
            c["japanese_skill"] = sk.name

        if card["default_leader_skill_id"]:
            c["center_skill"] = self.fetch_lskill_name(card["default_leader_skill_id"])

        return c

    def disconnect(self):
        self.c.close()

def main(db):
    k = UnitDB(db, "names.json")
    code.interact(local={"DB": k})

if __name__ == "__main__":
    import plac; plac.call(main)
