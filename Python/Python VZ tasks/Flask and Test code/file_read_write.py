import json


class File_r_w:

    def __init__(self,filename1):
        self.filename = filename1

    def change_myfile(self):

        r = open(self.filename, 'r')
        # print r.readline()
        dic = r.readline()
        dics = str(dic)
        newdic = dics.replace("\\", "")
        newdic2 = eval(newdic)
        newdic2 = json.dumps(newdic2)

        print '\n newdic = '
        print newdic
        print '\n newdic2 = '
        print newdic2
        print '\n newdic2 json = '
        print json.dumps(newdic2)
        ww = open ('newmyfile.txt', 'w')
        ww.write(newdic2)

ff = File_r_w('myfile.txt')
ff.change_myfile()
