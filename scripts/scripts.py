from brownie import accounts, network, Wei
import os, json, shutil, glob
from pinatapy import PinataPy

pinata = PinataPy(os.getenv("PINATA_KEY"), os.getenv("PINATA_SECRET_KEY"))

IPFS_URL = "https://ipfs.io/ipfs/"

development_networks = ["development"]


def is_development():
    return get_network() in development_networks


def get_network():
    return network.show_active()


def get_account():
    if is_development():
        return accounts[0]
    else:
        return accounts.load("test_account")


def get_balance():
    return get_account().balance()


def get_balance_in_eth():
    return Wei(get_balance()).to("ether")


def get_publish_source():
    if is_development():
        return False
    else:
        return True


def get_last_deploy(network_number="4"):
    with open("build/deployments/map.json", "r") as file:
        deploy_map = file.read()
        deploy_map = json.loads(deploy_map)
        return deploy_map[network_number]["nft"][-1]


def upload_file(path):
    ipfs_cid = pinata.pin_file_to_ipfs(path)["IpfsHash"]

    return IPFS_URL + ipfs_cid


def ls_only_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def copy_files_to_subdirectory(path):
    try:
        os.mkdir(path + "copy/")
    except FileExistsError:
        pass
    files = ls_only_files(path)
    i = 0
    for file in files:
        shutil.copy(path + file, path + "upload/" + str(i))
        i += 1


def upload_dir(path):
    ipfs_cid = pinata.pin_file_to_ipfs(path, {"wrapWithDirectory": "true"})["IpfsHash"]

    return IPFS_URL + ipfs_cid


def rm_files_in_dir(files):
    for file in files:
        os.remove(file)
