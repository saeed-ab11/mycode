# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import json

# create the application object
callback = Flask(__name__)


# use decorators to link the function to a url
@callback.route('/')
def home():
    return render_template("example.html")
    # return "Hello World"


my_dict = {'/newFirmware': [('notificationType', 'accountName', 'participantName', 'firmwareList'),
                            ('firmwareName', 'participantName', 'launchDate',
                             'releaseNote', 'model', 'make', 'fromVersion', 'toVersion'),
                            "New firmware notification result"],
           '/upgradeStarted': [('notificationType', 'accountName', 'participantName', 'firmwareName', 'upgradeId',
                                'resultCode', 'resultReason', 'finishTime'), (), 'Upgrade started notification result'],
           '/upgradeFinished': [
               ('notificationType', 'accountName', 'participantName', 'firmwareName', 'upgradeId', 'deviceList'),
               ('imei', 'status'), 'Upgrade finished notification result']
           }


def get_test_data(key):
    return my_dict.get(key)


@callback.route('/upgradeFinished', methods=['POST'])
@callback.route('/upgradeStarted', methods=['POST'])
@callback.route('/newFirmware', methods=['POST'])
def callbackFirmware():
    # General
    code = 200

    api_name = request.url_rule.rule
    my_test_data = get_test_data(api_name)

    items_tuple = my_test_data[0]
    fw_tuple = my_test_data[1]

    response = {"status": "success", "message": my_test_data[2]}
    fw_result_agg = []

    try:
        # Load the data from request
        js_data = json.loads(request.data)
        # Get missing or redundant keys
        check_keys_result = set(items_tuple) ^ set(js_data.keys())
        # Check and raise if have
        if check_keys_result:
            raise Exception("Redundant or missing fields: {}".format(str(tuple(check_keys_result))))

        for item in js_data.keys():
            if not js_data.get(item, ""):
                raise Exception("Missing value: {}".format(str(item)))

            if (item =='notificationType') or (js_data.get(item) != api_name):
                raise Exception("The value of {} must be: {}".format(str(item), str(api_name)))


        idx = 0

        if api_name == '/newFirmware':
            second_dict = "firmwareList"
        elif api_name == '/upgradeFinished':
            second_dict = "deviceList"
        else:
            second_dict = None

        if second_dict is not None:
            for fw_dict in js_data.get(second_dict):
                # Get missing or redundant keys for sublevel
                _local_fw_res = set(fw_tuple) ^ set(fw_dict.keys())
                # if something
                if _local_fw_res:
                    # Write with index
                    fw_result_agg.append({"fields": list(_local_fw_res), "index": idx})

                for item in fw_dict.keys():
                    if not fw_dict.get(item, ""):
                        raise Exception("Missing value: {} , 'index': {}".format(str(item), str(idx)))

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


if __name__ == '__main__':
    callback.run(host="0.0.0.0", port=8082, debug=False)
