import os
from scripts.scripts import *


METADATA_TEMPLATE = {
    "name": "",
    "description": os.getenv("TOKEN_DESC"),
    "image": "",
    "attributes": [
        {"trait_type": "Width", "value": 2227},
        {"trait_type": "Height", "value": 4821},
    ],
}


def gen_metadata(list_img):

    for img in list_img:
        metadata_name = os.path.split(img)[1]
        print(f"Gen metadata for {img}")

        metadata = METADATA_TEMPLATE
        metadata["name"] = (
            str(os.path.splitext(metadata_name)[0]).replace("_", " ").capitalize()
        )
        metadata["image"] = upload_file("img/" + str(img))

        print(f"Saving img {img}")
        with open("metadata/" + metadata_name + ".json", "w") as metadata_file:
            json.dump(metadata, metadata_file, indent=4)


def upload_metadata(list_metadata):
    list_URI = []
    for file in list_metadata:
        list_URI.append(upload_file("metadata/" + file))
    return list_URI
