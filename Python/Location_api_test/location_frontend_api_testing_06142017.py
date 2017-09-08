# import request library
import requests

# import json library
import json
from Practices.get_token import get_token_fun

requests.packages.urllib3.disable_warnings()

# specify url
base_url = 'https://152.198.0.166/loc/v1'


def locations_post_api(account_name, headers,imei,mdn):
    api = '/locations'
    # call rest api
    url = base_url + api
    print("POST ", url)

    response = {}

    payload = {"deviceList": [{"id": imei, "kind": "meid", "mdn": mdn}],
               "accuracyMode": "0",
               "cacheMode": "2",
               "accountName": account_name
               }

    print('POST data: ' + str(payload))
    print('Request Headers: ' + str(headers))

    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        print('status_code= ' + str(resp.status_code))
        print(resp.text)

        return resp.text

    except Exception as e:
        response["errorMsg"] = str(e)
        print("Exception happened! ->{}".format(e))


def run_test_plan():
    headers = {"Content-Type": "application/json", "VZ-M2M-Token": str(get_token_fun())}
    account_name = "1223334444-12345"
    imei = "AB0DEF10002001"
    mdn = "9568427504"

    locations_post_api(account_name, headers, imei, mdn)


if __name__ == '__main__':
    run_test_plan()
