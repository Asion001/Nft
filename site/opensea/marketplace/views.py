from django.shortcuts import render
import requests, json, time


def index(request):
    tokens = []
    contract = "0x9c88c9257E0dEb48FeB0D1f3d851a7374e0445Ac"
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


def get_token_info(contract, id):
    url = "https://testnets-api.opensea.io/asset/"
    answer = json.loads(requests.request("GET", url + contract + "/" + str(id)).text)
    return answer
