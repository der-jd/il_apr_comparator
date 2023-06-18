import time

import requests

import aws

# Scrape CakeDefi with https://www.browse.ai/

URL_CAKEDEFI_LM = "https://app.cakedefi.com/liquidity-mining"
COIN_PAIRS_MAX_NUMBER_OF_ROWS = 10
ROBOT_LIST_NAME = "Coin_Pairs_LM_APR"
ROBOT_LIST_NAME_COINPAIR_COLUMN = "coin_pair"
API_BASE_URL = "https://api.browse.ai/v2" # API docu: https://www.browse.ai/docs/api/v2


def get_aprs_from_cakedefi() -> list[dict]:
    print("Use browse.ai to get the APR values from CakeDefi...")
    data = _run_robot()
    data = _retrieve_task(data['id'])

    result = []
    for pair in data['result']['capturedLists'][ROBOT_LIST_NAME]:
        symbols = pair[ROBOT_LIST_NAME_COINPAIR_COLUMN].split('-')
        result.append({
            "symbols": pair[ROBOT_LIST_NAME_COINPAIR_COLUMN],
            "coin_1": {
                "id": "",
                "symbol": symbols[0],
                "name": ""
            },
            "coin_2": {
                "id": "",
                "symbol": symbols[1],
                "name": ""
            },
            "apr": pair['apr'][:-1] # remove the last character (% sign)
        })
    return result


def _run_robot() -> dict:
    print("Run the robot for scraping the CakeDefi Liquidity mining website...")

    robot_id = aws.get_parameter_value("/browse-ai/robot-id")
    api_key = aws.get_parameter_value("/browse-ai/api-key")
    url = f"{API_BASE_URL}/robots/{robot_id}/tasks"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "inputParameters": {
            "originUrl": URL_CAKEDEFI_LM,
            "coin_pairs_lm_apr_limit": COIN_PAIRS_MAX_NUMBER_OF_ROWS
        }
    }

    print(f"Call {url}...")
    try:
        response = requests.post(url, headers = headers, data = data, timeout = 10)
        response.raise_for_status()
    except (requests.exceptions.RequestException, ValueError) as err:
        raise RuntimeError(f"ERROR: API call to start browse.ai robot failed!\n{str(err)}") from err

    return response.json()


def _retrieve_task(task_id: str) -> dict:
    print("Wait until the task for scraping is finished...")

    robot_id = aws.get_parameter_value("/browse-ai/robot-id")
    api_key = aws.get_parameter_value("/browse-ai/api-key")
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

            if data['status'] == "failed":
                raise RuntimeError(f"ERROR: Task of the browse.ai robot failed!\n{response.status_code} {response.reason}")

            if data['status'] == "successful":
                return data
        except (requests.exceptions.RequestException, ValueError) as err:
            raise RuntimeError(f"ERROR: API call to retrieve task of the browse.ai robot failed!\n{str(err)}") from err

        time.sleep(5)
