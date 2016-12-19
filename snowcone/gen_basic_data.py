import json
import syncstate
import os
import sukutomo
import traceback
import gamestate
import config

ASSERT_KEYS = {
    "card_image",
    "card_idolized_image",
    "clean_ur",
    "clean_ur_idolized",
    "round_card_image",
    "round_card_idolized_image",
    "transparent_image",
    "transparent_image_idolized"}

def main(unitdb, imsync_db=None):
    if imsync_db is not None:
        DB = syncstate.State(imsync_db)
    else:
        DB = None

    GS = gamestate.UnitDB(unitdb, "names.json")

    if config.SUKUTOMO_TOKEN is None:
        token = sukutomo.grant()
        print("🔑    ", token)
    else:
        token = config.SUKUTOMO_TOKEN

    have = set(sukutomo.extant_ids())
    new  = set(GS.get_valid_card_numbers()) - have

    for ordinal in new:
        card = GS.skt_card_struct(ordinal)

        try:
            ret = sukutomo.create_card(ordinal, card, {}, token)

            if DB:
                if isinstance(ret, dict):
                    for k in ASSERT_KEYS:
                        if k not in ret:
                            ret[k] = None
                DB.ingest_api_object(ret)

            print("📝    ", ordinal)
        except:
            print("☠️    ", ordinal)
            traceback.print_exc()

    if DB:
        DB.disconnect()

if __name__ == '__main__':
    import plac; plac.call(main)
