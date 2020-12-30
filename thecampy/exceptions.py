class ThecampyException(Exception):
    pass

class ThecampyValueError(ThecampyException):
    pass

class ThecampyReqError(ThecampyException): #Request오류들
    pass