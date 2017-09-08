# import request library
import requests
import re

# import json library
import json
from xlwt import Workbook, easyxf

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

# base_url = 'http://10.141.141.10:443/fota/v1'


base_url = 'http://96.239.197.121:443/fota/v1'


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
        result_to_file(i, account_name, api, 'GET', 'Get subscription by account name', url, headers, "n/a", response)
        return response.text

    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)


def callback_api(callback, account_name, i, headers):
    api = '/callback'

    # call rest api
    url = base_url + api
    print url
    payload = {"callback": callback, "accountName": account_name}
    print 'POST data: ' + str(payload)
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        # print 'status_code= ' + str(response.status_code)
        result_to_file(i, account_name, api, 'POST', 'Update callback address', url, headers, payload, response)
        # response.text
    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)


def devices_api(account_name, i, headers):
    api = '/devices'
    # call rest api
    url = base_url + api + '/' + account_name

    print url
    try:
        response = requests.get(url)
        print 'status_code= ' + str(response.status_code)
        print response.text
        result_to_file(i, account_name, api, 'GET', 'Get account devices information', url, headers, "n/a", response)
        device_imei_list = []

        for d in response.json():
            device_imei_list.append(d['imei'])

        # account_imei_list = [d['imei'] for d in devices_api_response]

        return response.json(), device_imei_list, response.status_code

    except Exception, err_msg:
        code = 400
        response["errorCode"] = "400"
        response["error message"] = str(err_msg)


def assign_licenses_api(device_imei_list, account_name, i, headers):
    api = '/licenses'
    full_api = api + "/" + account_name + '/assign'

    response = {}
    # call rest api
    url = base_url + full_api
    print url

    payload = {"deviceList": device_imei_list}
    unidict_payload = {"deviceList": [x.encode('utf-8') for x in device_imei_list]}
    # unidict = {k.decode('utf8'): v.decode('utf8') for k, v in strdict.items()}

    print 'POST data: ' + str(unidict_payload)
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers)

        print 'status_code= ' + str(resp.status_code)
        result_to_file(i, account_name, api, 'POST', 'Assign fota licenses to devices', url, headers, unidict_payload,
                       resp)
        # response.text
        print resp.json()
        return resp.json(), resp.status_code

    except Exception, err_msg:
        response["errorCode"] = resp.status_code
        response["error message"] = str(err_msg)


def remove_licenses_api(device_imei_list, account_name, i, headers):
    api = '/licenses'
    full_api = api + "/" + account_name + '/remove'

    response = {}
    # call rest api
    url = base_url + full_api
    print url

    payload = {"deviceList": device_imei_list}

    unidict_payload = {"deviceList": [x.encode('utf-8') for x in device_imei_list]}
    #
    # print "encoded= " + str(unidict)

    print 'POST data: ' + str(unidict_payload)
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers)

        print 'status_code= ' + str(resp.status_code)
        result_to_file(i, account_name, api, 'POST', 'Remove fota licenses to devices', url, headers, unidict_payload,
                       resp)
        # response.text
        print resp.json()
        return resp.json()

    except Exception, err_msg:
        response["errorCode"] = resp.status_code
        response["error message"] = str(err_msg)


def licenses_api(account_name, i, headers):
    api = '/licenses'
    full_api = api + "/" + account_name

    response = {}
    # call rest api
    url = base_url + full_api
    print url

    try:
        resp = requests.get(url)

        print 'status_code= ' + str(resp.status_code)
        result_to_file(i, account_name, api, 'GET', 'Summarize fota licenses assignment', url, headers, "n/a",
                       resp)
        # response.text
        print resp.json()
        return resp.json()

    except Exception, err_msg:
        response["errorCode"] = resp.status_code
        response["error message"] = str(err_msg)


def upgrades_schedule_api(device_imei_list, account_name, StartDate, firmwareName, participantName,i, headers):
    api = '/upgrades'

    response = {}
    # call rest api
    url = base_url + api
    print url

    payload = {"deviceList": device_imei_list, "StartDate": StartDate, "firmwareName":firmwareName,
               "participantName":participantName,"accountName":account_name}

    unidict_payload = {"deviceList": [x.encode('utf-8') for x in device_imei_list], "StartDate": StartDate,
                       "firmwareName":firmwareName, "participantName":participantName,"accountName":account_name}

    print 'POST data: ' + str(unidict_payload)
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers)

        print 'status_code= ' + str(resp.status_code)
        result_to_file(i, account_name, api, 'POST', 'Schedule a firmware upgrade', url, headers, unidict_payload,
                       resp)
        # response.text
        print resp.json()
        return resp.json(), resp.status_code

    except Exception, err_msg:
        response["errorCode"] = resp.status_code
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


def test_plan(account_name,participantName, i, headers):
    # supscription_api_response = supscriptions_api_acc(account_name, i, headers)
    # callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)

    devices_api_response, device_imei_list, response_code = devices_api(account_name, i, headers)
    assign_licenses_api_response, assign_licenses_api_status_code = assign_licenses_api(device_imei_list, account_name,
                                                                                     i + 1, headers)
    licenses_api_response = licenses_api(account_name, i + 2, headers)

    upgrades_schedule_api(device_imei_list, account_name, StartDate, firmwareName, participantName, i+3, headers)

    remove_licenses_api_response = remove_licenses_api(device_imei_list, account_name, i + 3, headers)



    # if re.match("4[0-9]{2}",str(assign_licenses_api_status_code)):
    #     remove_licenses_api_response = remove_licenses_api(device_imei_list, account_name, i + 1, headers)
    #     assign_licenses_api_response, assign_licenses_api_status_code = assign_licenses_api(device_imei_list,
    #                                                                                         account_name, i + 2,
    #                                                                                        headers)


    # licenses_api_response = licenses_api(account_name, i + 2, headers)
    # upgrades_api_response = upgrades_api(account_name, i + 3, headers)
    # reports_api_response = reports_api(account_name, i + 4, headers)
    #

def run_test_plan():
    headers = {"Content-Type": "application/json"}
    api_numbers_to_test = 4
    subscriptions_list, response_code = supscriptions_api(headers)

    if re.match("2[0-9]{2}", str(response_code)):
        print subscriptions_list

        i = 2
        for subscriber in subscriptions_list:
            test_plan(subscriber.get("accountName"), subscriber.get("participantName"), i, headers)
            i += api_numbers_to_test
        #
        #
        # account_name_list = []
        #
        # for subscription in subscriptions_list:
        #     account_name_list.append(subscription['accountName'])
        #
        #     print account_name_list
        # i = 2
        # for account_name in account_name_list:
        #     # [participantName participantName = subscriptions_list[participantName] if subscriptions_list['account_name'] == account_name]
        #
        #
        #
        #     participantName = [d['participantName'] for d in subscriptions_list if d['account_name'] == account_name]
        #
        #
        #     print 'participantName= ', participantName
        #
        #     test_plan(account_name, participantName,  i, headers)
        #     i += api_numbers_to_test
        account_names = ['1111111111-11111', '1111111115-11115']
        account_info = {}

        for account in account_names:
            for subscriber in subscriptions_list:
                if subscriber.get("accountName") == account:
                    account_info['participant'] = subscriber.get("participantName")
                    account_info['account'] = account
                    break

        print account_info
        # O (n) ^ 2
if __name__ == '__main__':
    run_test_plan()
    wb.save('Test result.xls')



# # dict2 = eval(response.text)
# # print 'response data value= ' + str(dict2['data'])
#
# # print 'response data value= ' + str(response.json['data'])
#
# print 'response text= ' + str(eval(response.text))
# print 'response json= ' + str(response.json)
# print 'response header= ' + str(response.headers)
#
# print 'response Content-Type= ' + str(response.headers['Content-Type'])
#
# print 'response Content-Type= ' + str(response.headers.get('content-type'))
#
#
# # Get the headers of a given URL
# the_head = requests.head(base_url)
# print '\nresponse head=' + '\n head status_code= ' + str(the_head.status_code) +  \
#       '\n head text= ' + str(the_head.text) + '\n head headers= ' +  str(the_head.headers)
#
# url2 = base_url + '/newFirmware'
#
# headers = {'content-type': 'application/json'}
#
# response_new_firmware = requests.post(url2, data=json.dumps(payload), headers=headers)
# print '\nresponse_new_firmware= ' + str(response_new_firmware.json)
