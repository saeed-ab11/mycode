#import request library
import requests

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
sheet1.write(0,0,'No.',style3)
sheet1.col(0).width = 1000
sheet1.write(0,1,'Account Name',style3)
sheet1.col(1).width = 4000
sheet1.write(0,2,'API',style3)
sheet1.col(2).width = 3000
sheet1.write(0,3,'HTTP Method',style3)
sheet1.col(3).width = 3000
sheet1.write(0,4,'Test case description',style3)
sheet1.col(4).width = 8000
sheet1.write(0,5,'Request',style3)
sheet1.col(5).width = 13000
sheet1.write(0,6,'Request Header',style3)
sheet1.col(6).width = 7000
sheet1.write(0,7,'Body data for API',style3)
sheet1.col(7).width = 10000
sheet1.write(0,8,'Response',style3)
sheet1.col(8).width = 10000
sheet1.write(0,9,'Result',style3)
sheet1.col(9).width = 2000




#specify url

# base_url = 'http://10.141.141.10:443/fota/v1'
base_url = 'http://96.239.197.121:443/fota/v1'


def supscriptions_api(headers):
  api = '/subscriptions'
  # call rest api
  url = base_url + api

  print url
  try:
    response = requests.get(url)

    print 'status_code= ' + str(response.status_code)
    result_to_file(1, " ", api, 'GET', 'List all subscriptions', url, headers, "n/a", response)
    return response.text

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
    result_to_file(i, account_name, api, 'POST', 'Update callback address', url,headers, "n/a", response)
    # response.text
  except:
      code = 400
      response["errorCode"] = "400"
      response["error message"] = str(err_msg)


def devices_api(account_name, i, headers):
    pass

def result_to_file(i, account_name, api, http_method, description, url, headers, body, response):
    sheet1.write(i, 0, i)
    sheet1.write(i, 1, account_name)
    sheet1.write(i, 2, str(api))
    sheet1.write(i, 3, http_method)
    sheet1.write(i, 4, description)
    sheet1.write(i, 5, url)
    sheet1.write(i, 6, str(headers))
    sheet1.write(i, 7, body)

    sheet1.write(i, 8, response.text)
    if (response.status_code == 200):
      sheet1.write(i, 9, response.status_code, style1)
    else:
      sheet1.write(i, 9, response.status_code, style2)


def test_plan(account_name,i, headers):
    supscription_api_response = supscriptions_api_acc(account_name,i, headers)
    callback_api_response = callback_api("http://0.0.0.0", account_name,i+1, headers)
    devices_api_response = devices_api(account_name, i + 1, headers)

    callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)
    callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)
    callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)
    callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)
    callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)
    callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)
    callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)
    callback_api_response = callback_api("http://0.0.0.0", account_name, i + 1, headers)





def run_test_plan():
    headers = {"Content-Type": "application/json"}
    api_numbers_to_test = 2
    subscriptions_list = supscriptions_api(headers)

    if subscriptions_list != '404 page not found': # will be changed
        subscriptions_list = eval(subscriptions_list)
        print subscriptions_list

    account_name_list = []

    for subscription in subscriptions_list:
        account_name_list.append(subscription['accountName'])
        print account_name_list
    i = 2
    for account_name in account_name_list:
        test_plan(account_name, i, headers)
        i += api_numbers_to_test



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
