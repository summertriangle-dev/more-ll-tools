import requests
import json
import getpass
import datetime
import os
from config import *

def pull(url):
    rsp = requests.get(url)
    rsp.raise_for_status()

    out = rsp.json()
    for card_info in out["results"]:
        yield card_info

    if out.get("next"):
        yield from pull(out["next"])

    raise StopIteration()

def extant_ids():
    rsp = requests.get(SUKUTOMO_URL + "/api/cardids/")
    rsp.raise_for_status()

    return rsp.json()

def grant():
    if os.getenv("TC4_DRY_RUN"):
        return None

    data = {
        "grant_type": "password",
        "username": SUKUTOMO_UID,
        "client_id": SUKUTOMO_CLIENT_ID,
        "client_secret": SUKUTOMO_CLIENT_SECRET,
    }

    if SUKUTOMO_PASSWORD is not None:
        data["password"] = SUKUTOMO_PASSWORD
    else:
        data["password"] = getpass.getpass("The Token Grabbler stands before you. Please give it a password so it may grabble your token> "),

    r = requests.post("{0}/o/token/".format(SUKUTOMO_URL), data=data).json()
    token = r["access_token"]
    return token

def update_card(ordinal, data, files, token):
    # print(data, files)

    if token is None:
        return None

    r = requests.patch("{0}/api/cards/{1}/".format(SUKUTOMO_URL, ordinal),
        files=files, data=data, headers={"Authorization": "Bearer " + token})

    r.raise_for_status()
    return r.json()

def delete_card(ordinal, token):
    if token is None:
        return None

    r = requests.delete("{0}/api/cards/{1}/".format(SUKUTOMO_URL, ordinal),
        headers={"Authorization": "Bearer " + token})

    r.raise_for_status()
    return r.json()

def create_card(ordinal, data, files, token):
    # print(data, files)

    if token is None:
        return None

    r = requests.post("{0}/api/cards/".format(SUKUTOMO_URL),
        files=files, data=data, headers={"Authorization": "Bearer " + token})

    r.raise_for_status()
    return r.json()
