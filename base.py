import sqlite3


class WorkBase:

    def __init__(self, namebase):
        self.__base = sqlite3.connect(namebase)
        self.check_base_start()
        self.__cur = self.__base.cursor()
        self.__cur.execute("""select * from sqlite_master where type = 'table'""")

    def check_base_start(self):
        if self.__base:
            print('DateBase connected...OK')
        elif self.__base is None:
            print('DateBase connected...NOT OK')
