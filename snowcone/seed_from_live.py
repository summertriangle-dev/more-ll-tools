import requests
import json
import syncstate
from sukutomo import pull

def main(out):
    DB = syncstate.State(out)

    for ao in pull("http://schoolido.lu/api/cards/"):
        DB.ingest_api_object(ao)

    DB.disconnect()

if __name__ == '__main__':
    import plac; plac.call(main)