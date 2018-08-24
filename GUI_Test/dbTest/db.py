import sqlite3
conn = sqlite3.connect('LOG_Temp.db')
c = conn.cursor()


def create_DB():
    # Create table
    c.execute('''CREATE TABLE LOG_RETURNS
                (logID int,
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


if __name__ == '__main__':
    # create_DB()
    massInput()
    read()
    conn.close()
