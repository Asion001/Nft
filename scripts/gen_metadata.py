from brownie import nft
from scripts.scripts import *
import requests, os

PINTA_API_URL = "https://api.pinata.cloud/"
IPFS_URL = "https://ipfs.io/ipfs/"

METADATA_TEMPLATE = {
    "name": "",
    "description": os.getenv("TOKEN_DESC"),
    "image": "",
}


def main():
    add_metadata()


def add_metadata():
    gen_metadata(get_list_img())


def get_list_img():
    return os.listdir("img/")


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

        upload_file("img/" + img)


def upload_file(path):
    ipfs_add = os.popen(f"ipfs add --cid-version=1 {path}")
    ipfs_cid = str(ipfs_add.readlines()).split()[1]
    print(ipfs_cid)
    ipfs_add.close()
    file_name = os.path.splitext(os.path.split(path)[1])[0]
    ipfs_pin = os.popen(
        f"ipfs pin remote add --service=Pinata --name {file_name} {ipfs_cid}"
    )
    ipfs_pin.close()
    return IPFS_URL + ipfs_cid
