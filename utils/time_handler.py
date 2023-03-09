# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Union
from datetime import datetime, date, time, timedelta
from pytz import timezone, UnknownTimeZoneError


DATETIME_LIKE_TYPE = Union[datetime, date, time, float, int, str]
DATETIME_PARSE_FORMAT = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%SZ",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S.%f%z",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S %f",
    "%Y-%m-%d %H:%M:%S %f%z",
    "%Y-%m-%d %H:%M:%S%Z",
    "%c",
    "%S",
    "%Y-%m-%d",
    # YMD other than ISO
    "%Y%m%d",
    "%Y.%m.%d",
    # Popular MDY formats
    "%m/%d/%Y",
    "%m/%d/%y",
    # DMY with full year
    "%d %m %Y",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d/%m %Y",
    "%d.%m.%Y",
    "%d. %m. %Y",
    "%d %b %Y",
    "%d %B %Y",
    "%d. %b %Y",
    "%d. %B %Y",
    # MDY with full year
    "%b %d %Y",
    "%b %dst %Y",
    "%b %dnd %Y",
    "%b %drd %Y",
    "%b %dth %Y",
    "%b %d, %Y",
    "%b %dst, %Y",
    "%b %dnd, %Y",
    "%b %drd, %Y",
    "%b %dth, %Y",
    "%B %d %Y",
    "%B %dst %Y",
    "%B %dnd %Y",
    "%B %drd %Y",
    "%B %dth %Y",
    "%B %d, %Y",
    "%B %dst, %Y",
    "%B %dnd, %Y",
    "%B %drd, %Y",
    "%B %dth, %Y",
    # DMY with 2-digit year
    "%d %m %y",
    "%d-%m-%y",
    "%d/%m/%y",
    "%d/%m-%y",
    "%d.%m.%y",
    "%d. %m. %y",
    "%d %b %y",
    "%d %B %y",
    "%d. %b %y",
    "%d. %B %y",
    # MDY with 2-digit year
    "%b %dst %y",
    "%b %dnd %y",
    "%b %drd %y",
    "%b %dth %y",
    "%B %dst %y",
    "%B %dnd %y",
    "%B %drd %y",
    "%B %dth %y"
]


class HumanDateTime(object):

    @classmethod
    def from_any(cls, any_dt: DATETIME_LIKE_TYPE):
        """把传入的时间解析成datetime对象

        :param any_dt: 可以是datetime、date、time对象，或秒级或毫秒时间戳，或字符串
        :rtype: datetime
        """
        if any_dt is None:
            return datetime.now().replace(microsecond=0)
        elif isinstance(any_dt, datetime):
            return any_dt
        elif isinstance(any_dt, date):
            return datetime(
                year=any_dt.year, month=any_dt.month, day=any_dt.day
            )
        elif isinstance(any_dt, time):
            return datetime.now().replace(
                hour=any_dt.hour, minute=any_dt.minute, second=any_dt.second,
                microsecond=any_dt.microsecond
            )
        elif isinstance(any_dt, (float, int)):
            return cls.timestamp_parse(any_dt)
        elif isinstance(any_dt, str):
            try:
                tt = float(any_dt)
                return cls.timestamp_parse(tt)
            except ValueError:
                return cls.str_parse(any_dt)
        else:
            raise TypeError(f"Unknown datetime-like type: {type(any_dt)}")

    @classmethod
    def str_parse(cls, dt_str):
        """把传入的字符串成datetime对象，1个字符串可能符合多种解析格式，因此这里的转换可能与预期不符合

        :param str dt_str: 需要解析成datetime的字符串
        :rtype: datetime
        """
        for fmt in DATETIME_PARSE_FORMAT:
            try:
                return datetime.strptime(dt_str, fmt)
            except ValueError:
                pass
        else:
            raise ValueError(f'输入的时间格式不正确：{dt_str}')

    @classmethod
    def timestamp_parse(cls, dt_num: Union[float, int]):
        """把传入的时间戳成datetime对象

        :param dt_num: 需要解析成datetime的时间戳
        :rtype: datetime
        """
        if 100000000 <= dt_num < 100000000000:
            return datetime.fromtimestamp(dt_num)
        elif 100000000000 <= dt_num < 100000000000000:
            return datetime.fromtimestamp(dt_num / 1000)
        else:
            raise ValueError(f'时间戳超出范围：{dt_num}')

    @classmethod
    def today(cls):
        """今天零点

        :rtype: HumanDateTime
        """
        return cls(datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ))

    @classmethod
    def yesterday(cls):
        """昨天零点

        :rtype: HumanDateTime
        """
        return cls.today().sub(days=1)

    @classmethod
    def tomorrow(cls):
        """明天零点
        :rtype: HumanDateTime
        """
        return cls.today().add(days=1)

    def __init__(self, origin: Union[DATETIME_LIKE_TYPE, HumanDateTime] = None):
        """
        :param origin: 可以是HumanDateTime、datetime、date、time对象，或秒级或毫秒时间戳，或字符串
        """
        if isinstance(origin, HumanDateTime):
            self.origin = origin.origin
            self.dt: datetime = origin.dt
        else:
            self.origin = origin
            self.dt: datetime = self.from_any(self.origin)

    def human_time(self, fmt='%Y-%m-%d %H:%M:%S'):
        """返回日期时间的格式化字符串

        :param str fmt: 字符串格式
        :rtype: str
        """
        return self.dt.strftime(fmt)

    def human_date(self, fmt='%Y-%m-%d'):
        """返回日期的格式化字符串

        :param str fmt: 字符串格式
        :rtype: str
        """
        return self.dt.date().strftime(fmt)

    def timestamp(self):
        """返回秒级时间戳

        :rtype: int
        """
        return int(self.dt.timestamp())

    def milli_timestamp(self):
        """返回毫秒级时间戳

        :rtype: int
        """
        return int(self.dt.timestamp() * 1000)

    def micro_timestamp(self):
        """返回微秒级时间戳

        :rtype: int
        """
        return int(self.dt.timestamp() * 1000000)

    def add(self, days=0, weeks=0, hours=0, minutes=0, seconds=0):
        """时间加法

        :param int days: 天数
        :param int weeks: 周数
        :param int hours: 小时数
        :param int minutes: 分钟数
        :param int seconds: 秒数
        :rtype: HumanDateTime
        """
        return type(self)(
            self.dt + timedelta(
                days=days, weeks=weeks,
                hours=hours, minutes=minutes, seconds=seconds
            )
        )

    def sub(self, days=0, weeks=0, hours=0, minutes=0, seconds=0):
        """时间减法

        :param int days: 天数
        :param int weeks: 周数
        :param int hours: 小时数
        :param int minutes: 分钟数
        :param int seconds: 秒数
        :rtype: HumanDateTime
        """
        return self.add(
            days=-days, weeks=-weeks,
            hours=-hours, minutes=-minutes, seconds=-seconds
        )

    def approach(self, any_dt: Union[DATETIME_LIKE_TYPE, HumanDateTime], seconds):
        """检查是否在误差范围内

        :param any_dt: 可以是datetime、date、time对象，或秒级或毫秒时间戳，或字符串
        :param int seconds: 秒数
        :rtype: bool
        """
        return abs(self.dt.timestamp() - type(self)(any_dt).dt.timestamp()) <= seconds

    def astimezone(self, tz):
        """
        返回指定时区的时间对象
        :param str tz: 标准时区，如 America/New_York，Asia/Shanghai 等
        :return : HumanDateTime 对象
        """
        try:
            dt_tz = timezone(tz)
        except UnknownTimeZoneError:
            raise ValueError("时区参数错误")

        return type(self)(self.dt.astimezone(tz=dt_tz))

    def __lt__(self, other: Union[DATETIME_LIKE_TYPE, HumanDateTime]):
        return self.dt.timestamp() < type(self)(other).dt.timestamp()

    def __le__(self, other: Union[DATETIME_LIKE_TYPE, HumanDateTime]):
        return self.dt.timestamp() <= type(self)(other).dt.timestamp()

    def __gt__(self, other: Union[DATETIME_LIKE_TYPE, HumanDateTime]):
        return self.dt.timestamp() > type(self)(other).dt.timestamp()

    def __ge__(self, other: Union[DATETIME_LIKE_TYPE, HumanDateTime]):
        return self.dt.timestamp() >= type(self)(other).dt.timestamp()

    def __eq__(self, other: Union[DATETIME_LIKE_TYPE, HumanDateTime]):
        return self.dt.timestamp() == type(self)(other).dt.timestamp()

    def __ne__(self, other: Union[DATETIME_LIKE_TYPE, HumanDateTime]):
        return self.dt.timestamp() != type(self)(other).dt.timestamp()

    def __str__(self):
        return self.human_time()

    def __getattr__(self, item):
        return getattr(self.dt, item)

    def __repr__(self):
        return f"HumanDateTime(origin={repr(self.origin)}, dt={repr(self.dt)})"
