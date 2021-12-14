from brownie import accounts, network, Wei, project
import os, json

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
