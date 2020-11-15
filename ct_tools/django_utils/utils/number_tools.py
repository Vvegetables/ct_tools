"""
数字处理函数
"""
import copy
from decimal import Decimal
import re

# 返回千分位
to_thousands = lambda x: format(Decimal('{:.2f}'.format(x)), ',')

# 格式化函数
def _format(num, percent=False, thousands=False):
    """
    @param: percent: 是否附带%
    @param: thousands: 是否附带千分位
    """
    if percent:
        return "%.2f%%" % num
    else:
        if isinstance(num, (float, int)):
            if thousands:
                if isinstance(num, float):
                    return re.sub(r"(\d)(?=(\d\d\d)+(?!\d))", r"\1,", "%.2f" % num)
                else:
                    return re.sub(r"(\d)(?=(\d\d\d)+(?!\d))", r"\1,", str(num))
            else:
                if isinstance(num, float):
                    return "%.2f" % num
                else:
                    return num
        else:
            return num

# 数字业务逻辑包
class NumsUtil:

    @classmethod
    def percent(cls, a, b):
        if isinstance(a, str):
            a = int(a[:-1])
        if a is None:
            return
        v = round(cls.no0div(a * 100, b), 2)
        if v <= 0:
            v = 1
        return "%.2f%%" % v

    @classmethod
    def no0div(cls, a, b):
        try:
            if b == 0:
                return 0
            else:
                if isinstance(a, str):
                    if "+" in a:
                        a = int(a[:-1])
                    else:
                        a = float(a)
                if isinstance(b, str):
                    if "+" in b:
                        b = int(b[:-1])
                    else:
                        b = float(b)
                return a / b
        except:
            return 0

    @classmethod
    def place0handle(cls, v, vlist, reverse=True):
        _vlist = copy.deepcopy(vlist)
        _vlist = [
            float(
                _[:-1]
                if isinstance(_, str)
                else 0
                if (_ is None or _ < 0)
                else _
            )
            for _ in _vlist
        ]

        v = float(
            v[:-1]
            if isinstance(v, str)
            else 0
            if (v is None or v < 0)
            else v
        )

        _vlist.append(v)
        _vlist.sort(reverse=reverse)
        place = _vlist.index(v) + 1
        if v <= 0:
            return str(place) + "+"
        else:
            return place

    @classmethod
    def place_str_minus(cls, a, b):
        if a is None or b is None:
            return
        if isinstance(a, str):
            if not a[-1:].isdigit():
                a = int(a[:-1])
            else:
                a = int(a)
        if isinstance(b, str):
            if not b[-1:].isdigit():
                b = int(b[:-1])
            else:
                b = int(b)
        return a - b

    @classmethod
    def rank_cmp(cls, a, b):
        if not a or not b:
            return 2
        if isinstance(a, str):
            a = int(a[:-1])
        if isinstance(b, str):
            b = int(b[:-1])
        if a - b > 0.000001:
            return 3
        elif -0.000001 < a - b <= 0.000001:
            return 2
        else:
            return 1

    @classmethod
    def num_cmp(cls, a, b):
        try:
            a = float(a)
            b = float(b)
            if a - b > 0.000001:
                return 1
            elif -0.000001 < a - b <= 0.000001:
                return 2
            else:
                return 3
        except:
            return 2