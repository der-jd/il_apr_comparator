"""
Scrape website with https://www.browse.ai/.

ATTENTION:
Robot is not reliable! Sometimes no result at all; sometimes result with empty table.
"""

import os
import time

import requests

import aws


ROBOT_LIST_NAME = "Coin_Pairs_LM_APR"
ROBOT_LIST_NAME_COINPAIR_COLUMN = "coin_pair"
API_BASE_URL = "https://api.browse.ai/v2" # API docu: https://www.browse.ai/docs/api/v2


def get_apr() -> list[dict]:
    print("Use web service browse.ai to get the APR values...")
    data = _run_robot()
    data = _retrieve_task(data['result']['id'])

    result = []
    for pair in data['result']['capturedLists'][ROBOT_LIST_NAME]:
        print(f"Found: {pair[ROBOT_LIST_NAME_COINPAIR_COLUMN]} --> {pair['apr']}")
        symbols = pair[ROBOT_LIST_NAME_COINPAIR_COLUMN]
        result.append({
            "symbols": symbols,
            "coin_1": {
                "id": "",
                "symbol": symbols.split('-')[0],
                "name": ""
            },
            "coin_2": {
                "id": "",
                "symbol": symbols.split('-')[1],
                "name": ""
            },
            "apr": pair['apr'][:-1] # remove the last character (% sign)
        })
    return result


def _run_robot() -> dict:
    print("Run the robot for scraping...")

    robot_id = aws.get_parameter_value(os.environ.get('BROWSE_AI_ROBOT_ID'))
    api_key = aws.get_parameter_value(os.environ.get('BROWSE_AI_API_KEY'))
    url = f"{API_BASE_URL}/robots/{robot_id}/tasks"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Call {url}...")
    try:
        response = requests.post(url, headers = headers, timeout = 10)
        response.raise_for_status()
    except (requests.exceptions.RequestException, ValueError) as err:
        raise RuntimeError(f"ERROR: API call to start browse.ai robot failed!\n{str(err)}") from err

    return response.json()


def _retrieve_task(task_id: str) -> dict:
    print("Wait until the task for scraping is finished...")

    robot_id = aws.get_parameter_value(os.environ.get('BROWSE_AI_ROBOT_ID'))
    api_key = aws.get_parameter_value(os.environ.get('BROWSE_AI_API_KEY'))
    url = f"{API_BASE_URL}/robots/{robot_id}/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    while True:
        print(f"Call {url}...")
        try:
            response = requests.get(url, headers = headers, timeout = 10)
            response.raise_for_status()
            data = response.json()

            if data['result']['status'] == "failed":
                raise RuntimeError(f"ERROR: Task of the browse.ai robot failed!\n{response.status_code} {response.reason}")

            if data['result']['status'] == "successful":
                print("Task finished successfully!")
                return data
        except (requests.exceptions.RequestException, ValueError) as err:
            raise RuntimeError(f"ERROR: API call to retrieve task of the browse.ai robot failed!\n{str(err)}") from err

        time.sleep(5)
