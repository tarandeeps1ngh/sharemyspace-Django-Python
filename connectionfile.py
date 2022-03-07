from pymysql import *

class connectionfile:
    def ConnectMe(self):
        conn = Connect("127.0.0.1", "root", '', "project")
        return conn