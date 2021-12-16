from django.shortcuts import render
from etherscan import Etherscan
import requests, json, time, os
from django.views.decorators.cache import cache_page

contract = "0x3CD7c02229301529d23899BFB4e5B20764BBAEfb"
opensea_assets_url = "https://testnets.opensea.io/assets/"
etherscan_url = "https://rinkeby.etherscan.io/tx/"


@cache_page(60 * 15)
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
                "url": f"{opensea_assets_url}{contract}/{id}",
                "description": answer.get("description"),
                "traits": answer.get("traits"),
                "image_original_url": answer.get("image_original_url"),
                "collection": answer["collection"].get("slug"),
            }
        )
        time.sleep(0.8)
        id += 1
        answer = get_token_info(contract, id)

    return render(
        request,
        "gallery/index.html",
        {"tokens": tokens, "contract": contract},
    )


@cache_page(60 * 15)
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
                "link": etherscan_url + tx.get("hash"),
            }
        )
        i += 1
    return render(
        request,
        "history/index.html",
        {"transactions": transactions, "contract": contract},
    )
