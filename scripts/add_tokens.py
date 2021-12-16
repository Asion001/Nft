from brownie import nft
from scripts.scripts import *


def main():
    for URI in upload_metadata(os.listdir("metadata/")):
        add_token(URI, acc)


def add_token(URI, acc):
    tx = nft[-1].addToken(acc, URI, {"from": acc})
    tx.wait(1)
