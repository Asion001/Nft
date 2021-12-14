from brownie import nft
from scripts.scripts import *


def main():
    deploy(os.getenv("TOKEN_NAME"), os.getenv("TOKEN_SYMBOL"))


def deploy(name, symbol):
    acc = get_account()
    contract = nft.deploy(
        name, symbol, {"from": acc}, publish_source=get_publish_source()
    )
    print(
        f'NFT "{contract.name()}({contract.symbol()}) deployed to {get_network()} network!'
    )
