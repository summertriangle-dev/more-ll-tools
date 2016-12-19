import requests
import json
import gamestate
from sukutomo import pull
import sukutomo
import config

def main(out, update=False):
    DB = gamestate.UnitDB(out, "names.json")

    if config.SUKUTOMO_TOKEN is None:
        token = sukutomo.grant()
        print("🔑    ", token)
    else:
        token = config.SUKUTOMO_TOKEN

    for ao in pull("http://schoolido.lu/api/cards/"):
        generated = DB.skt_card_struct(ao["id"])

        unmatch = []
        for key in generated:
            if key in {"name", "release_date", "idol"}:
                continue

            if ao.get(key) != generated.get(key):
                unmatch.append(key)

        if unmatch:
            print("🚫    ", ao["id"])
            for k in unmatch:
                print("    ...", k, ao.get(k), generated.get(k))

            if update:
                sukutomo.update_card(ao["id"], {k: generated[k] for k in unmatch}, {}, token)
        else:
            print("✅    ", ao["id"])

    DB.disconnect()
    print("If you didn't see any 🚫 s, the database is fine")

if __name__ == '__main__':
    import plac; plac.call(main)
