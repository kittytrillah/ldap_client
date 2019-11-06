import sqlite3


def table_create():
    try:
        sqliteConnection = sqlite3.connect('uldap.db')
        cursor = sqliteConnection.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS credentials (
                                               id integer PRIMARY KEY,
                                               username text NOT NULL,
                                               password text NOT NULL,
                                               server_address text NOT NULL,
                                               server_port text NOT NULL,
                                               use_ssl integer NOT NULL
                                           ); """)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def add(username, pwd, server_address, server_port, ssl_val):
    print("adding values to DB: ", username, pwd, server_address, server_port, ssl_val)
    sqliteConnection = sqlite3.connect('uldap.db')
    cursor = sqliteConnection.cursor()
    cursor.execute('''INSERT INTO credentials (username,password,server_address,server_port,use_ssl) VALUES (?,?,?,?,?)''', (username, pwd, server_address, server_port, ssl_val))
    sqliteConnection.commit()
    get()
    sqliteConnection.close()


def clear():
    sqliteConnection = sqlite3.connect('uldap.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("DROP TABLE credentials;")
    sqliteConnection.close()


def get():
    try:
        sqliteConnection = sqlite3.connect('uldap.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM credentials ORDER BY ROWID ASC LIMIT 1")
        m = cursor.fetchall()
        print("all data from DB: ", m)
        sqliteConnection.close()
        return m
    except sqlite3.OperationalError as error:
        list = [0]
        return list


def match_pass(val):
    try:
        sqliteConnection = sqlite3.connect('uldap.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT password FROM credentials")
        m = cursor.fetchall()
        sqliteConnection.close()
        return m
    except sqlite3.OperationalError as error:
        e_val = "error"
        return e_val