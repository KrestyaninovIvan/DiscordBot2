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

    def users_sum_time(self, name):
        return self.__cur.execute('SELECT userid, sum(time) FROM {} GROUP BY userid'.format(name)).fetchall()

    def games_sum_time(self, name):
        return self.__cur.execute('SELECT game, sum(time) FROM {} GROUP BY game'.format(name)).fetchall()

    def games_time_user(self, name, id, data):
        return self.__cur.execute("SELECT game, sum(time) FROM {} WHERE userid == ? AND datetime > ? GROUP BY game".format(name),(id, data)).fetchall()
    def games_user(self, name, id):
        return self.__cur.execute("SELECT game, sum(time) FROM {} WHERE userid == ? GROUP BY game".format(name),(id, )).fetchall()
