import boto3
import json
import random
import requests
import os
import time

from bs4 import BeautifulSoup
from typing import Dict, List

IN_STOCK_MSG = "Ship to Me"
FILE_PATH = os.getenv('FILE_PATH')
SNS_TOPIC = os.getenv('SNS_TOPIC')
QA = os.getenv('QA')


def get_endpoints_from_file(path: str) -> List[Dict[str, str]]:
    """Read in endpoints JSON file from the filepath."""
    with open(path, 'r') as f:
        res = f.read()
        return json.loads(res)


def request_endpoints(req_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Request each url in endpoint and return response text in dict."""
    for req_dict in req_list:
        url = req_dict["url"]
        r = requests.get(url)
        r.raise_for_status
        req_dict["response"] = r.text

        # sleep just to "play it cool" between requests
        time.sleep(random.uniform(1, 3))
    return req_list


def check_for_success(req_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Checks all requests for a success."""
    for req in req_list:
        req["available"] = is_available(req["response"])
    return req_list


def is_available(response_text: str) -> bool:
    """Return whether or not item is available."""
    soupish = BeautifulSoup(response_text, 'html.parser')\
        .find_all(attrs={'class': 'ship-mode-message'})
    for el in soupish:
        if el.text.strip() == IN_STOCK_MSG:
            return True
    return False


def publish(req_list: List[Dict[str, str]]) -> None:
    """Publish message to SNS to SMS delivery."""
    for req in req_list:
        if req["available"]:
            msg = f"Bruh, go buy {req['size']} lbs! {req['url']}"
            if bool(QA):
                print(msg)
            else:
                boto3.client('sns').publish(
                    TopicArn=SNS_TOPIC,
                    Message=msg,
                    MessageStructure='string'
                )


def run():
    """Run it (hands in the air, now, hands in the air)."""
    reqs = get_endpoints_from_file(FILE_PATH)
    reqs = request_endpoints(reqs)
    reqs = check_for_success(reqs)
    publish(reqs)
    print('ran successfully')


if __name__ == '__main__':
    run()
