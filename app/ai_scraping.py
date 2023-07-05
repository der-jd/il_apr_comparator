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
ROBOT_DOUBLE_CHECK  = True # If a task fails, try to run it once more before finally failing
# If the robot fails which sometimes happens even after a potential double check, the robot can be run again.
# This is additionally to the potential double check! That means a number of '2' here can lead with double check to maximum number of 4 runs in total.
# The robot is always run at least once, whatever number is defined here!
ROBOT_MAX_NUMBER_OF_TRIES = 2
API_BASE_URL = "https://api.browse.ai/v2" # API docu: https://www.browse.ai/docs/api/v2


def get_apr() -> list[dict]:
    print("Use web service browse.ai to get the APR values...")
    number_of_tries = 1
    while True:
        try:
            data = _run_robot()
            data = _retrieve_task(data['result']['id'])
            break
        except RuntimeError as err:
            if number_of_tries < ROBOT_MAX_NUMBER_OF_TRIES:
                number_of_tries += 1
                print(f"Run of the browse.ai robot failed but '{ROBOT_MAX_NUMBER_OF_TRIES}' runs are allowed, so try again...")
            else:
                raise RuntimeError("ERROR: Maximum number of tries exceeded!") from err

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

    # Call to AWS Parameter Store will automatically fail if the environment variable is empty
    robot_id = aws.get_parameter_value(os.environ.get('BROWSE_AI_ROBOT_ID')) # pyright: ignore [reportGeneralTypeIssues]
    api_key = aws.get_parameter_value(os.environ.get('BROWSE_AI_API_KEY')) # pyright: ignore [reportGeneralTypeIssues]
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

    # Call to AWS Parameter Store will automatically fail if the environment variable is empty
    robot_id = aws.get_parameter_value(os.environ.get('BROWSE_AI_ROBOT_ID')) # pyright: ignore [reportGeneralTypeIssues]
    api_key = aws.get_parameter_value(os.environ.get('BROWSE_AI_API_KEY')) # pyright: ignore [reportGeneralTypeIssues]
    url = f"{API_BASE_URL}/robots/{robot_id}/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    failure_allowed = ROBOT_DOUBLE_CHECK
    while True:
        print(f"Call {url}...")
        try:
            response = requests.get(url, headers = headers, timeout = 10)
            response.raise_for_status()
            data = response.json()

            if data['result']['status'] == "failed":
                if failure_allowed:
                    failure_allowed = False # failure is only allowed once
                    print("Task of the browse.ai robot failed once but 'double check' is activated, so try again...")
                else:
                    raise RuntimeError(f"ERROR: Task of the browse.ai robot failed!\n{response.status_code} {response.reason}")

            if data['result']['status'] == "successful":
                print("Task finished successfully!")
                return data
        except (requests.exceptions.RequestException, ValueError) as err:
            raise RuntimeError(f"ERROR: API call to retrieve task of the browse.ai robot failed!\n{str(err)}") from err

        time.sleep(10)
