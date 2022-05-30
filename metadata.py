from PIL import Image
from IPython.display import display
import random
import json
import os

from trait_rarity import *

# Generate metadata for each image
f = open(
    "./metadata/all-traits.json",
)
data = json.load(f)

IMAGES_BASE_URL = (
    "https://gateway.pinata.cloud/ipfs/QmPvUPaqy5LBQggKhUHNQE69LHmbFkFYbPxesXZrLxEiRd/"
)
PROJECT_NAME = "COOL PUNK"


def getAttribute(key, value):
    return {"trait_type": key, "value": value}


for i in data:
    token_id = i["tokenId"]
    token = {
        "image": IMAGES_BASE_URL + str(token_id) + ".jpeg",
        "tokenId": token_id,
        "name": PROJECT_NAME + " " + str(token_id),
        "attributes": [],
    }
    token["attributes"].append(getAttribute("Face", i["Face"]))
    token["attributes"].append(getAttribute("Ears", i["Ears"]))
    token["attributes"].append(getAttribute("Eyes", i["Eyes"]))
    token["attributes"].append(getAttribute("Hair", i["Hair"]))
    token["attributes"].append(getAttribute("Mouth", i["Mouth"]))
    token["attributes"].append(getAttribute("Nose", i["Nose"]))

    with open("./metadata/" + str(token_id) + ".json", "w") as outfile:
        json.dump(token, outfile, indent=4)
f.close()
