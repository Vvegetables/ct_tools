from decimal import Decimal
import re

to_thousands = lambda x: format(Decimal('{:.2f}'.format(x)), ',')

#格式化函数
def _format(num, percent=False, thousands=False):
    '''
    @param: percent: 是否附带%
    @param: thousands: 是否附带千分位
    '''
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
