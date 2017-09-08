
dict1 = ('notificationType','accountName','participantName','firmwareList')
dict2 = ('notificationType','accountName','firmwareList')

dict3 = {'notificationType':0,'accountName':0,'participantName':0,'firmwareList':0}

dict4 = {'notificationType':0,'participantName':0,'fiarmwareList':0}

print set(dict1) ^ set(dict2)

a = set(dict3.keys()) ^ set(dict4.keys())


print str(tuple(a))