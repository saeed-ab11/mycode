# import request library
import requests
import re

# import json library
import json
from xlwt import Workbook, easyxf
import datetime

# sheets styles
style1 = easyxf('pattern: pattern solid, fore_color green;')
style2 = easyxf('pattern: pattern solid, fore_color red;')
style3 = easyxf('pattern: pattern solid, fore_color yellow')
# specify the excel file
wb = Workbook()
sheet1 = wb.add_sheet('Test result')
sheet1.write(0, 0, 'No.', style3)
sheet1.col(0).width = 1000
sheet1.write(0, 1, 'Account Name', style3)
sheet1.col(1).width = 4000
sheet1.write(0, 2, 'API', style3)
sheet1.col(2).width = 3000
sheet1.write(0, 3, 'HTTP Method', style3)
sheet1.col(3).width = 3000
sheet1.write(0, 4, 'Test case description', style3)
sheet1.col(4).width = 8000
sheet1.write(0, 5, 'Request', style3)
sheet1.col(5).width = 13000
sheet1.write(0, 6, 'Request Header', style3)
sheet1.col(6).width = 7000
sheet1.write(0, 7, 'Body data for API', style3)
sheet1.col(7).width = 10000
sheet1.write(0, 8, 'Response', style3)
sheet1.col(8).width = 10000
sheet1.write(0, 9, 'Result', style3)
sheet1.col(9).width = 2000

# specify url

base_url = 'http://10.141.141.10:443/loc/v1'

# base_url = 'http://96.239.197.125:443/loc/v1'


def ping_api(headers):
    api = '/ping'
    # call rest api
    url = base_url + api
    response = {}
    print url
    try:
        resp = requests.get(url)

        print 'status_code= ' + str(resp.status_code)
        print resp.text

    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)

def create_account_api(headers):
    api = '/licUpdate'

    url = 'http://10.141.141.10:886/TSSubMgmt/action'+ api
    print url
    payload = '{"custId":"7777777775","accountNo":"77775","SKU":"Loc_mrc","TotalCount":199,"ForceCount":false,"txid":"igw-1475609599186-203"}'

    print payload
    resp = requests.post(url,data=payload, headers=headers)
    print 'status_code= ' + str(resp.status_code)
    print resp.text


def supscriptions_api(headers):
    api = '/subscriptions'
    # call rest api
    url = base_url + api
    response = {}
    print url
    try:
        response = requests.get(url)

        print 'status_code= ' + str(response.status_code)
        result_to_file(1, " ", api, 'GET', 'List all subscriptions', url, headers, "n/a", response)
        return response.json(), response.status_code

    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)


def supscriptions_api_acc(account_name, i, headers):
    api = '/subscriptions'
    # call rest api
    url = base_url + api + '/' + account_name

    print url
    try:
        response = requests.get(url)
        print 'status_code= ' + str(response.status_code)
        print response.text
        result_to_file(i, account_name, api, 'GET', 'Get a location subscription by account name', url, headers, "n/a", response)
        return response.text

    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)


def consents_api(account_name, i, headers):
    api = '/consents'
    # call rest api
    url = base_url + api + '/' + account_name

    response = {}

    print 'GET  ' + url
    try:
        resp = requests.get(url)
        print 'status_code= ' + str(resp.status_code)
        print resp.text

        result_to_file(i, account_name, api, 'GET', 'Get a consent exclusion by account name', url, headers, "n/a", resp)
        return resp.text

    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)


def consents_post_api(account_name, allDevice, exclusion, i, headers):
    api = '/consents'
    # call rest api
    url = base_url + api
    print 'POST  ' + url

    response = {}

    payload = {"accountName": account_name,"allDevice": allDevice, "exclusion": exclusion}
    print 'POST data: ' + str(payload)

    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers)
        print 'status_code= ' + str(resp.status_code)
        print resp.text

        result_to_file(i, account_name, api, 'POST', 'Update account consent exclusion', url, headers, payload, resp)
        return resp.text

    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)


def locations_post_api(account_name, i, headers):
    api = '/locations'
    # call rest api
    url = base_url + api
    print url

    response = {}


    payload = {"accountName": account_name, "accuracyMode": 0, "cacheMode": 1,
               "deviceList": [{"IMEI": "2222222222", "MDN": "4081112222"}]}

    print 'POST data: ' + str(payload)

    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers)
        print 'status_code= ' + str(resp.status_code)
        print resp.text

        result_to_file(i, account_name, api, 'POST', 'Obtain locations to devices', url, headers, payload, resp)
        return resp.text

    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)


def result_to_file(i, account_name, api, http_method, description, url, headers, body, response):

    sheet1.write(i, 0, i)
    sheet1.write(i, 1, account_name)
    sheet1.write(i, 2, str(api))
    sheet1.write(i, 3, http_method)
    sheet1.write(i, 4, description)
    sheet1.write(i, 5, url)
    sheet1.write(i, 6, str(headers))
    sheet1.write(i, 7, str(body))
    sheet1.write(i, 8, response.text)
    if re.match("2[0-9]{2}", str(response.status_code)):
        sheet1.write(i, 9, response.status_code, style1)
    else:
        sheet1.write(i, 9, response.status_code, style2)




def test_case_positive_1(account_name, fotaType, licenseCount, i, headers):
    supscription_api_response = supscriptions_api_acc(account_name, i, headers)
    consent_api_response = consents_api(account_name, i+1, headers)
    consent_post_api_response = consents_post_api(account_name, True, [], i + 2, headers)
    locations_post_api_response = locations_post_api(account_name, i + 3, headers)


# def test_case_positive_2(account_name, fotaType, licenseCount, i, headers):
#     supscription_api_response = supscriptions_api_acc(account_name, i, headers)
#     consent_api_response = consent_api(account_name, i+1, headers)
#     consent_post_api_response = consent_post_api(account_name, False, [], i + 2, headers)
#     locations_post_api_response = locations_post_api(account_name, i + 3, headers)
#
#
# def test_case_positive_3(account_name, fotaType, licenseCount, i, headers):
#     supscription_api_response = supscriptions_api_acc(account_name, i, headers)
#     consent_api_response = consent_api(account_name, i+1, headers)
#     consent_post_api_response = consent_post_api(account_name, False, ["2222222222"], i + 2, headers)
#     locations_post_api_response = locations_post_api(account_name, i + 3, headers)


def run_test_plan():
    headers = {"Content-Type": "application/json"}
    api_numbers_to_test = 4
    ping_api(headers)

    create_account_api(headers)
    subscriptions_list, response_code = supscriptions_api(headers)

    if re.match("2[0-9]{2}", str(response_code)):
        print subscriptions_list

        i = 2
        for subscriber in subscriptions_list:
            test_case_positive_1(subscriber.get("accountName"), subscriber.get("locType"),
                        subscriber.get("licenseCount"), i, headers)
            i += api_numbers_to_test

            # test_case_positive_2(subscriber.get("accountName"), subscriber.get("locType"),
            #             subscriber.get("licenseCount"), i, headers)
            # i += api_numbers_to_test
            #
            # test_case_positive_3(subscriber.get("accountName"), subscriber.get("locType"),
            #             subscriber.get("licenseCount"), i, headers)
            # i += api_numbers_to_test




if __name__ == '__main__':
    run_test_plan()
    wb.save('Test result_location.xls')
