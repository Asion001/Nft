from brownie import nft
from scripts.scripts import *
import os
from pinatapy import PinataPy

IPFS_URL = "https://ipfs.io/ipfs/"

METADATA_TEMPLATE = {
    "name": "",
    "description": os.getenv("TOKEN_DESC"),
    "image": "",
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
    ipfs_add = os.popen(f"ipfs add --cid-version=1 {path}")
    ipfs_cid = ipfs_add.readlines()
    ipfs_cid = ipfs_cid[0].split()[1]

    ipfs_add.close()

    file_name = os.path.splitext(os.path.split(path)[1])[0]
    ipfs_pin = os.popen(
        f"ipfs pin remote add --service=Pinata --name {file_name} {ipfs_cid}"
    )
    print(ipfs_pin.readline())
    ipfs_pin.close()

    return IPFS_URL + ipfs_cid


def add_token(URI, acc):
    tx = nft[-1].addToken(acc, URI, {"from": acc})
    tx.wait(1)
