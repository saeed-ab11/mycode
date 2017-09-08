# import request library
import requests
import re

# import json library
import json
import datetime


# base_url = 'http://96.239.197.125:443/loc/v1'


class location_test:

    def __init__(self,base_url,accountName):
        self.base_url = base_url
        self.api_dict = {}
        self.accountName = accountName

    def api_testing(self, ):
        pass

    def supscriptions_api(self,headers):
        api = '/subscriptions'
        # call rest api
        url = self.base_url + api
        response = {}
        print (url)
        try:
            response = requests.get(url)

            print ('status_code= ' + str(response.status_code))
            return response.json(), response.status_code

        except Exception as e:
            response["errorMsg"] = str(e)
            print("Exception happened! ->{}".format(e))


    def supscriptions_api_acc(self, account_name, i, headers):
        api = '/subscriptions'
        # call rest api
        url = self.base_url + api + '/' + account_name

        print (url)
        try:
            response = requests.get(url)
            print ('status_code= ' + str(response.status_code))
            print (response.text)
            return response.text


        except Exception as e:
            response["errorMsg"] = str(e)
            print("Exception happened! ->{}".format(e))


    def consents_api(self,account_name, i, headers):
        api = '/consents'
        # call rest api
        url = self.base_url + api + '/' + account_name

        response = {}

        print ('GET  ' + url)
        try:
            resp = requests.get(url)
            print ('status_code= ' + str(resp.status_code))
            print (resp.text)

            return resp.text


        except Exception as e:
            response["errorMsg"] = str(e)
            print("Exception happened! ->{}".format(e))


    def consents_post_api(self,selfaccount_name, allDevice, exclusion, i, headers):
        api = '/consents'
        # call rest api
        url = self.base_url + api
        print ('POST  ' + url)

        response = {}

        payload = {"accountName": self.account_name,"allDevice": allDevice, "exclusion": exclusion}
        print ('POST data: ' + str(payload))

        try:
            resp = requests.post(url, data=json.dumps(payload), headers=headers)
            print ('status_code= ' + str(resp.status_code))
            print (resp.text)

            return resp.text


        except Exception as e:
            response["errorMsg"] = str(e)
            print("Exception happened! ->{}".format(e))


    def locations_post_api(self,account_name, i, headers):
        api = '/locations'
        # call rest api
        url = self.base_url + api
        print (url)

        response = {}


        payload = {"accountName": account_name, "accuracyMode": 0, "cacheMode": 1,
                   "deviceList": [{"IMEI": "2222222222", "MDN": "4081112222"}]}

        print ('POST data: ' + str(payload))

        try:
            resp = requests.post(url, data=json.dumps(payload), headers=headers)
            print ('status_code= ' + str(resp.status_code))
            print (resp.text)

            return resp.text


        except Exception as e:
            response["errorMsg"] = str(e)
            print("Exception happened! ->{}".format(e))




if __name__ == '__main__':

    url_dict = {"iwk": "198.159.196.86"}
    api_list = ["subscriptions", "consents", "locations"]

    pos_test = location_test(url_dict("iwk"), api_list[0])

