import sqlite3


class dbManager:
    FILE_NAME = 'LOG_Temp.db'
    TABLE_NAME = 'LOG_RETURNS'

    def create_DB():
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            # Create table
            c.execute('''CREATE TABLE LOG_RETURNS
                        (logID int,
                        returnType text,
                        sender text,
                        reciever text,
                        logTime int,
                        dutyOfficer text,
                        serials text
                        )''')

            # Save (commit) the changes
            conn.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.

    def read():
        for row in c.execute('SELECT * FROM stocks ORDER BY price'):
            print(row)

    def input():
        t = ('RHAT',)
        c.execute('SELECT * FROM stocks WHERE symbol=?', t)

    def massInput():
        # Larger example that inserts many records at a time
        purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                     ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                     ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                     ]
        c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

    def newReturn(lst):
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO '+dbManager.TABLE_NAME+' VALUES (NULL,' +
                '?, '*(len(lst) - 1) + '?)',
                lst)

    def readReturn():
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            return c.execute('SELECT * FROM ' + dbManager.TABLE_NAME)


if __name__ == '__main__':
    dbManager.create_DB()
    # dbManager.massInput()
    # dbManager.read()
