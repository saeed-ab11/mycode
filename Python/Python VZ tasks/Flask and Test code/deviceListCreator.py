import json


def main():
    # l = []
    #
    #
    # fpath = "/Users/abolgmi/work/jmeter-scripts/test-input/fota/assign-license-multiple-device_48000.txt"
    #
    #
    # deviceId = "0000000000"
    #
    #
    # for i in range(1,55001):
    #     l.append(deviceId+str(i))
    #
    #
    # body = dict(deviceList=l)
    # # print json.dumps(body, indent=4)
    #
    # with open(fpath, 'w') as f:
    #     f.write(json.dumps(body))


    l2 = []
    fpath2 = "/Users/abolgmi/work/jmeter-scripts/test-input/fota/assign-license-multiple-device-same_55000.txt"
    deviceId2 = "000000000000005"

    for i in range(0, 55000):
        l2.append(deviceId2)

    body2 = dict(deviceList=l2)
    print json.dumps(body2, indent=4)
    with open(fpath2, 'w') as f2:
        f2.write(json.dumps(body2))

    l3 = []



    fpath3 = "/Users/abolgmi/work/jmeter-scripts/test-input/fota/schedule-upgrade-future-multiple-same_48000.txt"
    deviceId3 = "000000000000005"


    for i in range(0, 48000):
        l3.append(deviceId3)

    body3 = dict(deviceList=l3)

    body3.update({"participantName": "9999999999-99999", "StartDate": "2017-10-24"})

    print json.dumps(body3, indent=4)
    with open(fpath3, 'w') as f3:
        f3.write(json.dumps(body3))

l4=[]
fpath4 = "/Users/abolgmi/work/jmeter-scripts/test-input/fota/schedule-upgrade-future-multiple-same_48001.txt"
deviceId4 = "000000000000005"

for i in range(0, 48001):
    l4.append(deviceId4)

body4 = dict(deviceList=l4)

body4.update({"participantName": "9999999999-99999", "StartDate": "2017-10-24"})

print json.dumps(body4, indent=4)
with open(fpath4, 'w') as f4:
    f4.write(json.dumps(body4))

if __name__ == '__main__':
    main()
