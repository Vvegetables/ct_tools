import datetime
from typing import Generator, Optional, Union


# js时间转换
def js_date_2_system_date(date_: Union[int, str]) -> datetime:
    if "-" in str(date_):
        date_ = (datetime.datetime.strptime(date_[:10], "%Y-%m-%d") +
            datetime.timedelta(days=1)
        )
    else:
        date_ = int(date_)
        date_ = datetime.datetime.fromtimestamp(date_ / 1000)

    return date_

class GenerateUniqID:
    """
    用于前端作为唯一ID
    with GenerateUniqId() as uniq_id:
        id: int = next(uniq_id)
    """
    def __init__(self, start=None):
        self.func = self.generator(start)

    def __enter__(self):
        return self.func

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.func.send(1)
        except:
            pass

    def generator(self, start: Optional[int]=None):
        while True:
            if start is None:
                start = 1
            flag = yield start
            start += 1
            if flag is not None:
                break