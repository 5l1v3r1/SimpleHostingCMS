#!/usr/bin/python
import MySQLdb

'''
Use like this
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="user", # your username
                      passwd="pass", # your password
                      db="database") # name of the data base
'''

class DB:
    conn = None

    def connect(self):
        self.conn = MySQLdb.connect(host="localhost", # your host, usually localhost
                                 user="user", # your username
                                 passwd="pass", # your password
                                 db="database") # name of the data base

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.commit(sql)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.commit(sql)
        return cursor

    def commit(self, sql):
        if sql.startswith("SELECT") or sql.startswith("select"):
            pass
        else:
            self.conn.commit()

db = DB()
