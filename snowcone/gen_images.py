import json
import syncstate
import cardstacker4x
import os
import sukutomo
import traceback
import config
import binascii

def nonce():
    return binascii.hexlify(os.urandom(2)).decode("ascii")

def get_missing_formes(STACKER, ent):
    try:
        id = ent["ordinal"]
    except KeyError:
        id = ent["id"]
    vf = STACKER.valid_formes_for_unit(id)

    missing = []
    for f in vf:
        if ent[SCHOOLIDOLU_KEY_MAP[f]] is None:
            missing.append(f)

    return missing

SCHOOLIDOLU_KEY_MAP = {
    0: "card_image",
    1: "card_idolized_image",
    2: "clean_ur",
    3: "clean_ur_idolized",
    4: "round_card_image",
    5: "round_card_idolized_image",
    8: "transparent_image",
    9: "transparent_idolized_image",
}

PREFIX_FOR_FORME = {
    0: "card_",
    1: "card_",
    2: "card_",
    3: "card_",
    4: "icon_",
    5: "icon_",
    8: "navi_",
    9: "navi_",
}

SUFFIX_FOR_FORME = {
    0: "",
    1: "_t",
    2: "_c",
    3: "_ct",
    4: "",
    5: "_t",
    8: "",
    9: "_t",
}

def main(cache, out):
    DB      = syncstate.State(out)
    STACKER = cardstacker4x.CardStacker(cache)

    if config.SUKUTOMO_TOKEN is None:
        token = sukutomo.grant()
        print("🔑    ", token)
    else:
        token = config.SUKUTOMO_TOKEN

    for ent in DB.get_inconsistent_entries():
        missing = get_missing_formes(STACKER, ent)
        if not missing:
            print("✅    ", ent["ordinal"])
            DB.mark_entry_consistent(ent["ordinal"])
            continue

        print("🚫    ", ent["ordinal"], *[SCHOOLIDOLU_KEY_MAP[x] for x in missing])

        files = {}

        try:
            os.mkdir("imgs")
        except FileExistsError:
            pass

        for forme in missing:
            name = "{2}{0}{1}.png".format(ent["ordinal"],
                SUFFIX_FOR_FORME.get(forme, ""),
                PREFIX_FOR_FORME.get(forme, ""))
            fullpath = os.path.join("imgs", name)

            if not os.path.exists(fullpath):
                order = STACKER.layer_order_for_unit(int(ent["ordinal"]), forme)
                print(name)

                if len(order.order) == 1:
                    fullpath = os.path.join(cache, order.order[0].src)
                else:
                    STACKER.composite(order).save(fullpath)

            files[SCHOOLIDOLU_KEY_MAP[forme]] = (name, open(fullpath, "rb"))

        try:
            ret = sukutomo.update_card(ent["ordinal"], {}, files, token)
            DB.ingest_api_object(ret)
            if not get_missing_formes(STACKER, ret):
                print("📝    ", ent["ordinal"])
                DB.mark_entry_consistent(ent["ordinal"])
        except:
            print("☠️    ", ent["ordinal"])
            traceback.print_exc()
        finally:
            for name, fd in files.values():
                fd.close()

    DB.disconnect()

if __name__ == '__main__':
    import plac; plac.call(main)
