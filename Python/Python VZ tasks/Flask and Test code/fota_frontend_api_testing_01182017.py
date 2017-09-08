#import request library
import requests

# import json library
import json
from xlwt import Workbook

#specify the excel file
wb = Workbook()
sheet1 = wb.add_sheet('Test result')
sheet1.write(0,0,'No.')
sheet1.write(0,1,'API')
sheet1.col(1).width = 7000
sheet1.write(0,2,'HTTP Method')
sheet1.col(2).width = 3000
sheet1.write(0,3,'Test case description')
sheet1.col(3).width = 7000

sheet1.write(0,4,'Input Data for API')
sheet1.col(4).width = 7000
sheet1.write(0,5,'Pre-conditions')
sheet1.col(5).width = 7000
sheet1.write(0,6,'Input Data for API')
sheet1.col(6).width = 7000
sheet1.write(0,7,'Result')


#specify url

base_url = 'http://10.141.141.10:443/fota/v1'



def supscriptions_api():
  api = '/subscriptions'
  # call rest api
  url = base_url + api
  print url
  try:
    response = requests.get(url)

    print 'status_code= ' + str(response.status_code)
    sheet1.write(1, 0, '1')
    sheet1.write(1, 1, str(api))
    sheet1.write(1, 2, 'GET')

    return response.text
  except Exception, err_msg:
      code = 400
      response["errorCode"] = "400"
      response["error message"] = str(err_msg)
def supscriptions_api_acc(account_name):
  api = '/subscriptions'
  # call rest api
  url = base_url + api + '/' + account_name
  print url
  try:
    response = requests.get(url)
    print 'status_code= ' + str(response.status_code)
    print response.text
    return response.text

  except Exception, err_msg:
      code = 400
      response["errorCode"] = "400"
      response["error message"] = str(err_msg)


def callback_api(callback, accountName):
  api = '/callback'
  headers = {"Content-Type": "application/json"}
  # call rest api
  url = base_url + api
  print url
  payload = {"callback": callback, "accountName": accountName}
  print 'POST data: ' + str(payload)
  try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print 'status_code= ' + str(response.status_code)
    response.text
  except:
      code = 400
      response["errorCode"] = "400"
      response["error message"] = str(err_msg)



def test_plan(account_name):
  supscription_api_response = supscriptions_api_acc(account_name)
  callback_api_response = callback_api("http://0.0.0.0", account_name)



def run_test_plan():
  subscriptions_list = supscriptions_api()

  if subscriptions_list != '404 page not found': # will be changed
    subscriptions_list = eval(subscriptions_list)
    print subscriptions_list

    account_name_list = []

    for subscription in subscriptions_list:
      account_name_list.append(subscription['accountName'])
      print account_name_list

    for account_name in account_name_list:
      test_plan(account_name)


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
