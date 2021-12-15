from django.shortcuts import render
from etherscan import Etherscan
import requests, json, time, os

contract = "0x9c88c9257E0dEb48FeB0D1f3d851a7374e0445Ac"


def index(request):
    def get_token_info(contract, id):
        url = "https://testnets-api.opensea.io/asset/"
        answer = json.loads(
            requests.request("GET", url + contract + "/" + str(id)).text
        )
        return answer

    tokens = []
    id = 0
    answer = get_token_info(contract, id)

    while answer != {"success": False}:
        tokens.append(
            {
                "id": str(id),
                "name": answer.get("name"),
                "url": "https://testnets.opensea.io/assets/0x9c88c9257E0dEb48FeB0D1f3d851a7374e0445Ac/"
                + str(id),
                "description": answer.get("description"),
                "image_original_url": answer.get("image_original_url"),
            }
        )
        time.sleep(1)
        id += 1
        answer = get_token_info(contract, id)

    return render(
        request,
        "gallery/index.html",
        {"tokens": tokens},
    )


def history(request):
    def get_transactions_info(contract):
        eth = Etherscan(
            os.getenv("ETHERSCAN_TOKEN"), net="rinkeby"
        )  # key in quotation marks
        block_number_start = eth.get_block_number_by_timestamp(
            timestamp="1639314231", closest="before"
        )
        block_number_end = eth.get_block_number_by_timestamp(
            timestamp=int(time.time()), closest="before"
        )
        answer = eth.get_normal_txs_by_address(
            address=contract,
            startblock=block_number_start,
            endblock=block_number_end,
            sort="asc",
        )
        return answer

    transactions = []
    answer = get_transactions_info(contract)
    i = 1
    for tx in answer:
        tx_time = time.ctime(int(tx.get("timeStamp")))[7:]

        transactions.append(
            {
                "number": str(i),
                "blockNumber": tx.get("blockNumber"),
                "timeStamp": tx_time,
                "hash": tx.get("hash"),
                "from": tx.get("from"),
                "to": tx.get("to"),
                "value": tx.get("value"),
                "confirmations": tx.get("confirmations"),
                "link": "https://rinkeby.etherscan.io/tx/" + tx.get("hash"),
            }
        )
        i += 1
    return render(request, "history/index.html", {"transactions": transactions})
