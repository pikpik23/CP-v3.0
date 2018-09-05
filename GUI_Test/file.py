from csv import reader, writer
from collections import OrderedDict as OrdDic
import sqlite3
from jsmin import jsmin
from glob import glob
from csscompressor import compress


class MinifyFilesPre:
    def __init__(self, merge=False):
    
        # print(glob("resources/static/js_files/*.js"))
        file_names = glob("resources/static/js_files/*.js")
        file_names.remove("resources/static/js_files/full_version.js")
        # print(file_names)
        self.file_names = file_names
        self.merge = merge
        self.js = ""

    def save(self):
        """combines several js files together, with optional minification"""
        with open("resources/static/js_files/full_version.js", 'w') as w:
            w.write(self.js)

    def js_merge(self):
        """saves minified version to a single one"""
        if self.merge:
            js = ""
            for file_name in self.file_names:
                try:
                    # file_name = "resources/static/js_files/" + file_name
                    js += jsmin(open(file_name).read())
                    # js += '\n'
                except FileNotFoundError:
                    print(f"The file {file_name} could not be found")
                self.js = jsmin(js)

        else:
            for file_name in self.file_names:
                # file_name = "resources/static/js_files/" + file_name
                js = jsmin(open(file_name).read())
                open(file_name, 'w').write(js)

    @staticmethod
    def min_js_file(file_name):
        js = jsmin(open(file_name).read())
        open(file_name, 'w').write(js)

    @staticmethod
    def min_css_file(file_name):
        css = compress(open(file_name).read())
        open(file_name[:-4]+'.min.css', 'w').write(css)


    @staticmethod
    def get_js_files():
        file_names = glob("resources/static/js_files/*.js")
        file_names.remove("resources/static/js_files/full_version.js")


class DbManager:
    FILE_NAME = 'resources/static/LOG_Temp.db'
    TABLE_NAME = 'LOG_RETURNS'

    @staticmethod
    def create_db():
        with sqlite3.connect(DbManager.FILE_NAME) as conn:
            c = conn.cursor()
            # Create table
            c.execute('''CREATE TABLE LOG_RETURNS
                        (logID int,
                        returnType text,
                        sender text,
                        receiver text,
                        logTime int,
                        dutyOfficer text,
                        serials text
                        )''')

            conn.commit()

    @staticmethod
    def new_return(lst):
        with sqlite3.connect(DbManager.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO ' + DbManager.TABLE_NAME + ' VALUES (NULL,' +
                '?, ' * (len(lst) - 1) + '?)',
                lst)

    @staticmethod
    def read_return():
        with sqlite3.connect(DbManager.FILE_NAME) as conn:
            c = conn.cursor()
            return c.execute('SELECT * FROM ' + DbManager.TABLE_NAME)

    @staticmethod
    def find_index(log_id):
        with sqlite3.connect(DbManager.FILE_NAME) as conn:
            c = conn.cursor()
            sql_str = ("""SELECT * FROM """ +
                       DbManager.TABLE_NAME +
                       """ WHERE logID=?""")
            x = c.execute(sql_str, [str(log_id)])
            return x

    @staticmethod
    def get_first_index():
        with sqlite3.connect(DbManager.FILE_NAME) as conn:
            c = conn.cursor()
            sqlStr = ("""SELECT logID FROM """ +
                      DbManager.TABLE_NAME +
                      """ WHERE logID = (SELECT MAX(logID)  FROM """ +
                      DbManager.TABLE_NAME + ")")
            x = c.execute(sqlStr)
            for i in x:
                i = int(list(i)[0])
            return i

class File:

    @staticmethod
    def generate_css_min():
        MinifyFilesPre.min_css_file('resources/static/styles/main.css')

    @staticmethod
    def pre_merge(merge=False):

        if merge:
            tmp_file =  MinifyFilesPre()
            tmp_file.js_merge()
            tmp_file.save()
            # print(" * Updated js min merged")
        else:
            MinifyFilesPre.get_js_files()

    @staticmethod
    def get_first():
        return DbManager.get_first_index()

    @staticmethod
    def save_dic(dic):
        """ Saves the given dictionary of serials to a file """
        # print("start saving")
        w = writer(open("resources/files/serials.csv", "w"))
        w.writerow(['Return Name', 'Serials'])
        for name, serials in dic.items():
            lst = []
            if name == "Return Name":
                lst.append(name)
                lst.append(serials)
            else:
                for serial in serials:
                    if serial == "Return Name":
                        lst.append(serials)
                    else:
                        inner_lst = []
                        for cont in serials[serial]:
                            if cont == "options":
                                inner_lst.append(cont + ";;@@;;" +
                                                 ";;##;;".join(
                                                     serials
                                                     [serial]
                                                     ["options"]))
                            else:
                                inner_lst.append(
                                    cont + ";;@@;;" + serials[serial][cont])
                        lst.append(serial + ';;:::;;' + ";;!!!;;".join(inner_lst))
            w.writerow([(name), (';;,,,;;'.join(lst))])

    @staticmethod
    def read_dic():
        """ reads the dictionary of serials """
        # should return the original format
        dic = OrdDic()
        r = reader(open("resources/files/serials.csv", "r"))
        i = 0
        for row in r:
            if i:
                inner_dic = OrdDic()
                for serial in row[1].split(';;,,,;;'):
                    serial = serial.split(';;:::;;')
                    sub_dic = OrdDic()
                    for sub_serial in serial[1].split(';;!!!;;'):
                        sub_serial = sub_serial.split(";;@@;;")
                        if sub_serial[0] == 'options':
                            options = sub_serial[1].split(";;##;;")
                            sub_dic.update({sub_serial[0]: options})
                        else:
                            sub_dic.update(
                                {sub_serial[0]: sub_serial[1]})
                    inner_dic.update({serial[0]: sub_dic})
                # lst = row[1].split('\\')
                dic.update({row[0]: inner_dic})
            else:
                i += 1
            # print(" * Read Dictionary")
        return dic

    @staticmethod
    def read_legacy():
        """ reads the dictionary and returns it in the legacy format """
        serials = File.read_dic()
        final_dic = OrdDic()
        for name, dic in serials.items():
            inner_dic = OrdDic()
            for serial in dic:
                inner_dic.update({serial: dic[serial]['desc']})
            final_dic.update({name: inner_dic})
        return final_dic

    @staticmethod
    def read_locations():
        """ reads the file containing the locations """
        r = open("resources/files/locations.txt", "r")
        locations = r.read().split("\n")
        return locations

    @staticmethod
    def save_Locations(lst):
        w = open("resources/files/locations.txt", "w")
        w.write(lst)

    @staticmethod
    def read_callsigns():
        """ reads the file containing the callsigns """
        r = open("resources/files/callsigns.txt", "r")
        callsigns = r.read().split("\n")
        return callsigns

    @staticmethod
    def read_settings():
        """ reads the settings from file """
        r = open("resources/files/settings.txt", "r")
        settings = OrdDic()
        for option in r.read().split('\n'):
            try:
                option = option.split('\\')
                settings.update({option[0]: option[1]})
            except IndexError:
                pass
        return settings

    @staticmethod
    def save_settings(dic):
        """ saves the given settings (dictionary) to file """
        w = open("resources/files/settings.txt", "w")
        for sett, val in dic.items():
            w.write(sett + '\\' + val + '\n')

    @staticmethod
    def save_log(log):
        """ Saves the log to file """

        # print('\n\n\nsaving')
        '''
        s = Timer(10.0, save)
        s.daemon = True
        s.start()
        '''
        # w = writer(open("resources/static/logs.csv", 'w'))

        main_keys = [
            'name',
            'sender',
            'receiver',
            'time',
            'duty'
        ]

        # print(test)

        lst = []
        for key in main_keys:
            # print(key)
            lst.append(log[key])
        inn_lst = []
        for serial, val in log.items():
            if not (serial in main_keys):
                inn_lst.append(serial + '\\' + val)

        lst.append('||'.join(inn_lst))

        DbManager.new_return(lst)

    @staticmethod
    def load_log(log_id=None):
        """ loads the log file """
        # try:
        #     r = reader(open("resources/static/logs.csv", "r"))
        # except FileNotFoundError:
        #     w = open("resources/static/logs.csv", 'w')
        #     w.close()
        #     r = reader(open("resources/static/logs.csv", "r"))

        if log_id:
            x = DbManager.find_index(log_id)
        else:
            x = DbManager.read_return()

        local_log = []
        for row in x:
            ret = OrdDic()

            # print(row)
            ret.update({'logID': row[0]})
            ret.update({'name': row[1]})
            ret.update({'sender': row[2]})
            ret.update({'receiver': row[3]})
            ret.update({'time': row[4]})
            ret.update({'duty': row[5]})

            for serial_data in row[6:]:
                for serial in serial_data.split('||'):
                    ser, val = serial.split('\\')
                    val = "" + val
                    ret.update({ser: str(val)})
            local_log.append(ret)

        # OrdDic(reversed(list(local_log.items())))
        return local_log


if __name__ == '__main__':

    pass

    # File.pre_merge()

    # settings = File.read_settings()
    # File.save_settings(settings)
    # File.read_locations()
    # File.read_callsigns()
    # File.save_dic()
    # File.read_dic()

    # x = file()
    # x.save()

'''
INPUT TYPES

short text
location (contain a list of possible location)
long text
radio_button (list of possible options)

'''

"""
class admin_return:

    def init(self):
        self.serials_def = file.read()

"""
