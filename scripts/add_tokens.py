from brownie import nft
import pinatapy
from scripts.scripts import *
import os

from pinatapy import PinataPy

pinata = PinataPy(os.getenv("PINATA_KEY"), os.getenv("PINATA_SECRET_KEY"))

IPFS_URL = "https://ipfs.io/ipfs/"

METADATA_TEMPLATE = {
    "name": "",
    "description": os.getenv("TOKEN_DESC"),
    "image": "",
    "attributes": [
        {"trait_type": "Width", "value": 2227},
        {"trait_type": "Height", "value": 4821},
    ],
}


def main():
    gen_metadata(os.listdir("img/"))
    acc = get_account()
    for URI in upload_metadata(os.listdir("metadata/")):
        add_token(URI, acc)


def upload_metadata(list_metadata):
    list_URI = []
    for file in list_metadata:
        list_URI.append(upload_file("metadata/" + file))
    return list_URI


def gen_metadata(list_img):
    os.popen("rm metadata/*").close()

    for img in list_img:
        metadata_name = os.path.split(img)[1]
        print(f"Uploading file {img}")
        with open("metadata/" + metadata_name + ".json", "w") as metadata_file:
            metadata = METADATA_TEMPLATE
            metadata["name"] = (
                str(os.path.splitext(metadata_name)[0]).replace("_", " ").capitalize()
            )
            metadata["image"] = upload_file("img/" + str(img))
            json.dump(metadata, metadata_file, indent=4)


def upload_file(path):
    ipfs_cid = pinata.pin_file_to_ipfs(path)["IpfsHash"]

    return IPFS_URL + ipfs_cid


def add_token(URI, acc):
    tx = nft[-1].addToken(acc, URI, {"from": acc})
    tx.wait(1)
