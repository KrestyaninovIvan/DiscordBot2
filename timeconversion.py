from datetime import datetime as dt
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta


class SecondsConvert:
    __TODAY = dt.utcnow()

    def __init__(self, period=0):
        self.__period = period
        self.date = None
        self.period_out()
        self.__new_today()

    def period_out(self):
        self.date = (self.__TODAY - td(days=self.__period)).date()

    def __new_today(self):
        self.__TODAY = dt.utcnow()

    @property
    def to_day(self):
        return self.__TODAY

    @property
    def day(self):
        return self.__TODAY.day

    @property
    def month(self):
        return self.__TODAY.month

    @property
    def year(self):
        return self.__TODAY.year

    def date(self, datetime):
        return datetime.date()

    @property
    def months_minus(self):
        months = self.__TODAY - relativedelta(months=1)
        return months.date()

    @property
    def months_plus(self):
        months = self.__TODAY + relativedelta(months=1)
        return months.date()

    def time_to_second(self, time_start):
        game_time = self.__TODAY - time_start
        return game_time.seconds

    def __del__(self):
        print('SecondsConvert удален')


class DataOut:
    __SECOND_DAY = 86400
    __SECOND_HOUR = 3600
    __SECOND_MINUTE = 60

    def __init__(self, time=0):
        self.__time = time

    def time_update(self, time):
        self.__time = time

    def output_days(self, inscription=False):
        days = self.__time // self.__SECOND_DAY
        return self.inscription(inscription, days, 'День', 'Дня', 'Дней')

    def output_hours(self, inscription=False):
        hours = self.__time % self.__SECOND_DAY // self.__SECOND_HOUR
        return self.inscription(inscription, hours, 'Час', 'Часа', 'Часов')

    def output_minutes(self, inscription=False):
        minutes = self.__time % self.__SECOND_DAY
        minutes = minutes % self.__SECOND_HOUR
        minutes = minutes // self.__SECOND_MINUTE
        return self.inscription(inscription, minutes, 'Минуту', 'Минуты', 'Минут')

    @staticmethod
    def inscription(inscription, time, one, exception, plenty):
        if inscription:
            if time == 1:
                return f'{one}: {time}'
            elif time % 10 in [2, 3, 4]:
                return f'{exception}: {time}'
            else:
                return f'{plenty}: {time}'
        else:
            return time

    def __del__(self):
        print('DataOut удален')
