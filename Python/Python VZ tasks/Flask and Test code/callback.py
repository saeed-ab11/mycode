
#import the Flask class from the flask module
from flask import Flask , render_template, redirect, url_for, request
import json

# create the application object
callback = Flask(__name__)


# use decorators to link the function to a url
@callback.route('/')
def home():
    return render_template("example.html")
    #return "Hello World"



my_dict={ 'newFirmware': [('notificationType', 'accountName', 'participantName', 'firmwareList'),
                          ('firmwareName', 'participantName', 'launchDate',
                           'releaseNote', 'model', 'make', 'fromVersion','toVersion')],
          'upgradeStarted':('notificationType','accountName','participantName','firmwareName','upgradeId',
                             'resultCode','resultReason','finishTime'),
          'newFirmware':[('notificationType','accountName','participantName','firmwareName','upgradeId','deviceList'),
                         ('imei','status')]
          }

def get_test_data(key):
    return my_dict.get(key)

@callback.route('/upgradeFinished',methods=['POST'])
@callback.route('/upgradeStarted',methods=['POST'])
@callback.route('/newFirmware', methods=['POST'])
def callbackFirmware():
    # General
    code = 200
    response = {"status": "success", "message": "New firmware notification result"}

    api_name = request.url_rule.endpoint
    my_test_data = get_test_data(api_name)

    # Local vars
    kwargs = {}
    # List of fields for verification
    # items_tuple = ('notificationType', 'accountName', 'participantName', 'firmwareList')
    # fw_tuple = ('firmwareName', 'participantName', 'launchDate',
    #             'releaseNote', 'model', 'make', 'fromVersion','toVersion')

    items_tuple = my_test_data[0]
    fw_tuple = my_test_data[1]

    fw_result_agg = []

    try:
        # Load the data from request
        js_data = json.loads(request.data)
        # Get missing or redundant keys
        check_keys_result = set(items_tuple) ^ set(js_data.keys())
        # Check and raise if have
        if check_keys_result:
            raise Exception("Redundant or missing fields: {}".format(str(tuple(check_keys_result))))

        idx = 0
        for fw_dict in js_data.get("firmwareList"):
            # Get missing or redundant keys for sublevel
            _local_fw_res = set(fw_tuple) ^ set(fw_dict.keys())
            # if something
            if _local_fw_res:
                # Write with index
                fw_result_agg.append({"fields": list(_local_fw_res), "index":   idx})
            # Increase by one
            idx += 1

        # Check and raise if have
        if fw_result_agg:
            raise Exception("Redundant or missing fields in firmwareList: {}".format(str(tuple(fw_result_agg))))

    except Exception, err_msg:
        code = 400
        response["status"] = "fail"
        response["message"] = str(err_msg)
        # some impl

    finally:
        return json.dumps(response), code

    # try:
    #     jsdata = json.loads(request.data)
    # except ValueError:
    #     jsdata = json.loads(request.form.keys()[0])


    # jsdata = json.loads(request.data)
    #
    # itemsTuple = ('notificationType','accountName','participantName','firmwareList')
    #
    # for item in itemsTuple:
    #     if item not in jsdata:
    #         return json.dumps({"status": "fail", "errorCode": "400", "errorMessage": item + " is missing"})
    #
    #     # else:
    #     #     kwargs[item] = jsdata.get(item)
    #
    # # else:
    # #     for field in ('notificationType','accountName','participantName','firmwareList'):
    # #         kwargs[field] = jsdata.get(field)
    #
    # kwargs2 = {}
    # # jsdata2 = kwargs['firmwareList'][0]
    # jsdata2 = jsdata['firmwareList'][0]
    #
    # firmwareListTuple = ('firmwareName','participantName','launchDate','releaseNote','model','make','fromVersion',\
    #                      'toVersion')
    #
    # for item in firmwareListTuple:
    #     if item not in jsdata2:
    #         return json.dumps({"status": "fail", "errorCode": "400", "errorMessage": item + " is missing"})
    #
    #     for field2 in ('firmwareName','participantName','launchDate','releaseNote','model','make','fromVersion','toVersion'):
    #         kwargs2[field2] = jsdata2.get(field2)
    #
    #     return json.dumps({"status": "success", "message": "New firmware notification result"})
    #
    #         #return json.dumps(kwargs2['model'],200, {'Content-Type': 'application/json'},indent=4)
    #         # return jsdata


# @callback.route('/upgradeStarted',methods=['GET','POST'])
# def upgradeStarted():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid credentials. Please try again.'
#         else:
#             return redirect (url_for('home'))
#
#     return render_template("login.html", error=error)
#
#
# @callback.route('/upgradeFinished',methods=['GET','POST'])
# def upgradeFinished():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid credentials. Please try again.'
#         else:
#             return redirect (url_for('home'))
#
#     return render_template("login.html", error=error)

if __name__ == '__main__':
    callback.run(host="0.0.0.0", port=8082, debug=False)





