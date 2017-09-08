#import request library
import requests

# import json library
import json


#specify url
# base_url = 'http://0.0.0.0:8082'
# base_url = 'http://crappycode.herokuapp.com/task'
base_url = 'http://96.239.197.121:443/fota/v1'


account_name = '/1111111111-11111'

def supscription_api(account_name):
  api = '/subscription'





#call rest api
url = base_url + api + account_name
response = requests.get(url)


#print response
print 'reponse= '+ str(response)

print 'status_code= '+ str(response.status_code)
# dict2 = eval(response.text)
# print 'response data value= ' + str(dict2['data'])

# print 'response data value= ' + str(response.json['data'])

print 'response text= ' + str(eval(response.text))
print 'response json= ' + str(response.json)
print 'response header= ' + str(response.headers)

print 'response Content-Type= ' + str(response.headers['Content-Type'])

print 'response Content-Type= ' + str(response.headers.get('content-type'))


# Get the headers of a given URL
the_head = requests.head(base_url)
print '\nresponse head=' + '\n head status_code= ' + str(the_head.status_code) +  \
      '\n head text= ' + str(the_head.text) + '\n head headers= ' +  str(the_head.headers)

url2 = base_url + '/newFirmware'
payload = {
  "notificationType": "newFirmware",
  "accountName": "9999999999-9999",
  "participantName": "pn-9999999999-9999",
  "firmwareList": [
    {
      "firmwareName": "string",
      "participantName": "string",
      "launchDate": "2016-12-21",
      "releaseNote": "string",
      "model": "string",
      "make": "string",
      "fromVersion": "string",
      "toVersion": "string"
    },
    {
      "firmwareName": "string",
      "participantName": "string",
      "launchDate": "2016-12-21",
      "releaseNote": "string",
      "model": "string",
      "make": "string",
      "fromVersion": "string",
      "toVersion": "string"
    },
    {
      "firmwareName": "string",
      "participantName": "string",
      "launchDate": "2016-12-21",
      "releaseNote": "string",
      "model": "string",
      "make": "string",
      "fromVersion": "string",
      "toVersion": "string"
    }

  ]
}
headers = {'content-type': 'application/json'}

response_new_firmware = requests.post(url2, data=json.dumps(payload), headers=headers)
print '\nresponse_new_firmware= ' + str(response_new_firmware.json)
