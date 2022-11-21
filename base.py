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

    def user_time(self, name):
        return self.__cur.execute('SELECT userid, sum(time) FROM {} GROUP BY userid'.format(name)).fetchall()

    def user_time_period(self, name, period):
        return self.__cur.execute('SELECT userid, sum(time) FROM {} GROUP BY userid'.format(name),(period )).fetchall()

    def game_time(self, name):
        return self.__cur.execute('SELECT game, sum(time) FROM {} GROUP BY game'.format(name)).fetchall()

    def game_time_period(self, name, period):
        return self.__cur.execute('SELECT game, sum(time) FROM {} WHERE datetime > ? GROUP BY game'.format(name),(period, )).fetchall()

    def game_time_id_period(self, name, id, period):
        return self.__cur.execute("SELECT game, sum(time) FROM {} WHERE userid == ? AND datetime > ? GROUP BY game".format(name),(id, period)).fetchall()
    def game_time_id(self, name, id):
        return self.__cur.execute("SELECT game, sum(time) FROM {} WHERE userid == ? GROUP BY game".format(name),(id, )).fetchall()

    def create_base(self, name):

        self.__base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
        self.__base.commit()
        self.__base.execute(
            'CREATE TABLE IF NOT EXISTS {}(userid INT, game TEXT, datetime DATETIME, time INT)'.format(name + 'Game'))
        self.__base.commit()

    def base_update(self, name, id):
        warning = self.__cur.execute('SELECT count FROM {} WHERE userid == ?'.format(name), (id,)).fetchone()
        if warning is None:
            self.__base.execute('INSERT INTO {} VALUES(?, ?)'.format(name), (id, 1))
            self.__base.commit()
        else:
            self.__base.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name), (warning[1] + 1, id))
            self.__base.commit()

    def base_insert(self, name, user_id, game, time_start, game_time):
        self.__base.execute('INSERT INTO {} VALUES(?, ?, ?, ?)'.format(name), (user_id, game, time_start, game_time))
        self.__base.commit()

    def database_repetition(self,  name, user_id, game, time_start, game_time):
        search = self.__cur.execute("SELECT * FROM {} WHERE userid == ? AND datetime ==? GROUP BY game".format(name),
                           (user_id, time_start)).fetchall()
        if list(search) != 0:
            self.__base.execute('UPDATE {} SET time == ? WHERE userid == ? AND datetime == ?'.format(name), (game_time, user_id, time_start))
            self.__base.commit()
        else:
            self.base_insert(name, user_id, game, time_start, game_time)

    def execute_top_3(self, plug, table, months_minus, data):
        if plug:
            return self.__cur.execute('SELECT game, sum(time) FROM {} WHERE datetime BETWEEN ? AND ? GROUP BY game '
                                      'ORDER BY time DESC LIMIT 3'.format(table), (months_minus, data)).fetchall()
        else:
            return self.__cur.execute('SELECT userid, sum(time) FROM {} WHERE datetime BETWEEN ? AND ? GROUP BY userid '
                                      'ORDER BY time DESC LIMIT 3'.format(table), (months_minus, data)).fetchall()

    @property
    def fetchall(self):
        return self.__cur.fetchall()
