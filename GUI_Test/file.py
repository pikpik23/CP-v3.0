from csv import reader, writer
from collections import OrderedDict as OrdDic
import sqlite3
from jsmin import jsmin
from glob import glob
from csscompressor import compress


class MinifyFilesPre:
    def __init__(self, merge=False):

        file_names = glob("resources/static/js_files/*.js")
        file_names.remove("resources/static/js_files/full_version.js")
        self.file_names = file_names
        self.merge = merge
        self.js = ""

    def save(self):
        """combines several js files together, with optional minification"""
        with open("resources/static/js_files/full_version.js", 'w', newline="\n") as w:
            w.write(self.js)

    def js_merge(self):
        """saves minified version to a single one"""
        if self.merge:
            js = ""
            for file_name in self.file_names:
                try:
                    js += jsmin(open(file_name, newline="\n").read())
                except FileNotFoundError:
                    print(f"The file {file_name} could not be found")
                self.js = jsmin(js)

        else:
            for file_name in self.file_names:
                js = jsmin(open(file_name, newline="\n").read())
                open(file_name, 'w', newline="\n").write(js)

    @staticmethod
    def min_js_file(file_name):
        js = jsmin(open(file_name, newline="\n").read())
        open(file_name, 'w', newline="\n").write(js)

    @staticmethod
    def min_css_file(file_name):
        css = compress(open(file_name, newline="\n").read())
        open(file_name[:-4] + '.min.css', 'w', newline="\n").write(css)

    @staticmethod
    def get_js_files():
        file_names = glob("resources/static/js_files/*.js")
        file_names.remove("resources/static/js_files/full_version.js")


class DbManager:

    def __init__(self, fname=None, tname=None):
        if fname:
            self.FILE_NAME = fname
        else:
            self.FILE_NAME = 'resources/static/LOG_Temp.db'

        if tname:
            self.TABLE_NAME = tname
        else:
            self.TABLE_NAME = "'LOG_RETURNS'"


    def query_data(self, conditions, entries):
        try:
            with sqlite3.connect(self.FILE_NAME) as conn:
                c = conn.cursor()
                condition_order = ['logID',
                                   'returnType',
                                   'sender',
                                   'reciever',
                                   'logTime',
                                   'dutyOfficer',
                                   'net',
                                   'serials']

                cond_list = []
                cond_string_list = []
                for cond in condition_order:
                    val = ""
                    try:
                        val = conditions[cond]
                    except KeyError:
                        val = ""
                    for sub_val in val.split(", "):
                        cond_string_list.append(f"lower({cond}) LIKE ?")
                        sub_val = f"%{sub_val.lower()}%"
                        cond_list.append(sub_val)

                if conditions['other']:
                    for sub_val in conditions['other'].split(", "):
                        cond_string_list.append(f"lower(serials) LIKE ?")
                        sub_val = f"%{sub_val.lower()}%"
                        cond_list.append(sub_val)

                if conditions['logTimeFrom']:
                    if conditions['logTimeTo']:
                        cond_string_list.append("logTime>= ? AND logTime<= ?")
                        cond_list.append(conditions['logTimeFrom'])
                        cond_list.append(conditions['logTimeTo'])
                    else:
                        cond_string_list.append("logTime>= ?")
                        cond_list.append(conditions['logTimeFrom'])
                elif conditions['logTimeTo']:
                    cond_string_list.append("logTime <= ?")
                    cond_list.append(conditions['logTimeTo'])

                cond_string = ' AND '.join(cond_string_list)

                results = c.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE "
                                    f"{cond_string}"
                                    f" ORDER BY logID DESC LIMIT {entries}", cond_list)
                return results

        except sqlite3.OperationalError as e:
            print(e)

    def create_db(self, ret=False):
        with sqlite3.connect(self.FILE_NAME) as conn:
            c = conn.cursor()
            # Create table
            try:
                c.execute(f'''CREATE TABLE {self.TABLE_NAME} (
                                `logID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                `returnType`	text,
                                `sender`	text,
                                `reciever`	text,
                                `logTime`	integer,
                                `dutyOfficer`	text,
                                `net`	TEXT,
                                `serials`	text
                            );''')

                conn.commit()

            except sqlite3.OperationalError:
                print("The Db already exists")

            if ret:
                return self.read_return()

    def create_game_table(self, ret=False):
        with sqlite3.connect(self.FILE_NAME) as conn:
            c = conn.cursor()
            # Create table
            try:
                c.execute(f'''CREATE TABLE `{self.TABLE_NAME}` (
                    `GameID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    `Name`	TEXT DEFAULT '?',
                    `Rank`	TEXT DEFAULT '?',
                    `Pl`	TEXT DEFAULT '?',
                    `Score`	INTEGER DEFAULT 0,
                    `Time`	INTEGER
                );''')

                conn.commit()

            except sqlite3.OperationalError:
                print("The Db already exists")

            if ret:
                return self.read_return()


    def new_return(self, lst):
        try:
            with sqlite3.connect(self.FILE_NAME) as conn:
                c = conn.cursor()
                c.execute(
                    'INSERT INTO ' + self.TABLE_NAME + ' VALUES (NULL,' +
                    '?, ' * (len(lst) - 1) + '?)',
                    lst)
        except sqlite3.OperationalError as e:
            print(e)
            """
            if 'no such table' in str(e):
                if "game" in str(self.FILE_NAME):
                    print("MEME")
                    self.create_game_table()
                else:
                    self.create_db()
                self.new_return(lst)
            """


    def delete_return_byID(self, id):
        with sqlite3.connect(self.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute(f"DELETE FROM {self.TABLE_NAME} WHERE logID = {id}")


    def read_return(self, entries=None):
        try:
            with sqlite3.connect(self.FILE_NAME) as conn:
                c = conn.cursor()
                if entries:
                    results = c.execute(f"SELECT * FROM {self.TABLE_NAME} ORDER BY logID DESC LIMIT {entries}")
                else:
                    # should not be used but just here just in case
                    results = c.execute(f'SELECT * FROM {self.TABLE_NAME}')

                return results
        except sqlite3.OperationalError as e:
            if 'no such table' in str(e):
                DbManager.create_db(self)

    def read_game_score(self, entries=None):
        try:
            with sqlite3.connect(self.FILE_NAME) as conn:
                c = conn.cursor()
                if entries:
                    results = c.execute(f"SELECT * FROM {self.TABLE_NAME} ORDER BY Score DESC LIMIT {entries}")
                else:
                    # should not be used but just here just in case
                    results = c.execute(f'SELECT * FROM {self.TABLE_NAME} ORDER BY Score DESC')

                return results
        except sqlite3.OperationalError as e:
            if 'no such table' in str(e):
                DbManager.create_game_table(self)


    def find_index(self, log_id):
        with sqlite3.connect(self.FILE_NAME) as conn:
            c = conn.cursor()
            sql_str = ("""SELECT * FROM """ +
                       self.TABLE_NAME +
                       """ WHERE logID=?""")
            x = c.execute(sql_str, [str(log_id)])
            return x


    def get_first_index(self):

        with sqlite3.connect(self.FILE_NAME) as conn:
            i=""
            c = conn.cursor()
            sqlStr = ("""SELECT logID FROM """ +
                      self.TABLE_NAME +
                      """ WHERE logID = (SELECT MAX(logID)  FROM """ +
                      self.TABLE_NAME + ")")
            x = c.execute(sqlStr)
            for i in x:
                i = int(list(i)[0])
            try:
                return i
            except UnboundLocalError:
                return ""

    def update_record(self, lst, logID):
        with sqlite3.connect(self.FILE_NAME) as conn:
            c = conn.cursor()
            rowData = """returnType=?, sender=?, reciever=?, logTime=?, dutyOfficer=?, net=?, serials=?"""
            c.execute(
                'UPDATE ' + self.TABLE_NAME + ' SET ' + rowData + ' WHERE logID=' + logID,
                lst)


class File:

    @staticmethod
    def db_connect(sets):
        try:
            fname = sets['DB_FILE_NAME']
        except KeyError:
            fname = None

        try:
            tname = sets['DB_TABLE_NAME']
        except KeyError:
            tname = None

        conn = DbManager(fname=fname, tname=tname)
        return conn


    @staticmethod
    def generate_css_min():
        MinifyFilesPre.min_css_file('resources/static/styles/main.css')

    @staticmethod
    def pre_merge(merge=False):

        if merge:
            tmp_file = MinifyFilesPre()
            tmp_file.js_merge()
            tmp_file.save()
        else:
            MinifyFilesPre.get_js_files()

    @staticmethod
    def get_first(self):
        return self.get_first_index()

    @staticmethod
    def save_dic(dic):
        """ Saves the given dictionary of serials to a file """
        w = writer(open("resources/files/serials.csv", "w", newline="\n"))
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
        r = reader(open("resources/files/serials.csv", "r", newline="\n"))
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
        """ Depreciated reads the dictionary and returns it in the legacy format """
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
        r = open("resources/files/locations.txt", "r", newline="\n")
        locations = r.read().split("\n")
        return locations

    @staticmethod
    def save_Locations(lst):
        lst = '\n'.join(lst)
        w = open("resources/files/locations.txt", "w", newline="\n")
        w.write(lst)

    @staticmethod
    def save_callsigns(lst):
        lst = '\n'.join(lst)
        w = open("resources/files/callsigns.txt", "w", newline="\n")
        w.write(lst)

    @staticmethod
    def read_callsigns():
        """ reads the file containing the callsigns """
        r = open("resources/files/callsigns.txt", "r", newline="\n")
        callsigns = r.read().split("\n")
        return callsigns

    @staticmethod
    def read_settings():
        """ reads the settings from file """
        r = open("resources/files/settings.txt", "r", newline="\n")
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
        with open("resources/files/settings.txt", "w", newline="\n") as w:
            for sett, val in dic.items():
                w.write(sett + '\\' + val + '\n')

    @staticmethod
    def save_log(self, log, update=False):
        """ Saves the log to file """

        main_keys = [
            'name',
            'sender',
            'receiver',
            'time',
            'duty',
            'net'
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

        # print(lst)

        if update:
            self.update_record(lst, log['logID'])

        else:
            self.new_return(lst)

    @staticmethod
    def load_log_query(Db, query):

        print(query)
        x = list(Db.query_data(query, 100))

        local_log = list()
        for row in x:
            row = list(row)
            try:
                ret = OrdDic()

                ret.update({'logID': row[0]})
                ret.update({'name': row[1]})
                ret.update({'sender': row[2]})
                ret.update({'receiver': row[3]})
                ret.update({'time': row[4]})
                ret.update({'duty': row[5]})
                ret.update({'net': row[6]})

                for serial_data in row[7:]:
                    try:
                        for serial in serial_data.split('||'):
                            ser, val = serial.split('\\')
                            val = "" + val
                            ret.update({ser: str(val)})
                    except AttributeError:
                        print('The Db structure is incorrect')
                local_log.append(ret)

            except TypeError:
                print("none value in db")
        return local_log

    @staticmethod
    def load_log(Db, log_id=None):
        """ loads the log file """
        # try:
        #     r = reader(open("resources/static/logs.csv", "r"))
        # except FileNotFoundError:
        #     w = open("resources/static/logs.csv", 'w')
        #     w.close()
        #     r = reader(open("resources/static/logs.csv", "r"))

        if log_id:
            row = Db.find_index(log_id).fetchone()
            local_log = list()
            ret = None
            try:
                ret = OrdDic()

                ret.update({'logID': row[0]})
                ret.update({'name': row[1]})
                ret.update({'sender': row[2]})
                ret.update({'receiver': row[3]})
                ret.update({'time': fix_time(row[4])})
                ret.update({'duty': row[5]})
                ret.update({'net': row[6]})

                for serial_data in row[7:]:
                    try:
                        for serial in serial_data.split('||'):
                            ser, val = serial.split('\\')
                            val = "" + val
                            ret.update({ser: str(val)})
                    except AttributeError:
                        print('The Db structure is incorrect')

            except TypeError:
                pass  # This is handled upon return (it returns None type)

            return ret

        else:
            try:
                x = list(Db.read_return(entries=100))
            except TypeError:
                x = ""

            local_log = list()
            for row in x:
                row = list(row)

                try:
                    ret = OrdDic()

                    ret.update({'logID': row[0]})
                    ret.update({'name': row[1]})
                    ret.update({'sender': row[2]})
                    ret.update({'receiver': row[3]})
                    ret.update({'time': fix_time(row[4])})
                    ret.update({'duty': row[5]})
                    ret.update({'net': row[6]})

                    for serial_data in row[7:]:
                        try:
                            for serial in serial_data.split('||'):
                                ser, val = serial.split('\\')
                                val = "" + val
                                ret.update({ser: str(val)})
                        except AttributeError:
                            print('The Db structure is incorrect')
                    local_log.append(ret)

                except TypeError:
                    print("none value in db")

            return local_log

    @staticmethod
    def delete_log_byID(Db, id):
        Db.delete_return_byID(id)

def fix_time(dtg):
    if len(str(dtg)) == 6:
        return str(dtg)
    else:
        return str(f'0{dtg}')

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
