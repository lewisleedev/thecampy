from typing import NamedTuple
from . import exceptions

"""부대와 해당 부대 코드의 dictionary입니다.

Soldier class를 initialize 할때의 unit parameter는 아래의 dictionary의 해당 부대 key값과 정확히 일치해야합니다.
"""

unit_codes = {
    '1사단' : '20121290100',
    '2사단' : '20121490100',
    '3사단' : '20121590100',
    '5사단' : '20121690200',
    '6사단' : '20121590200',
    '7사단' : '20121390100',
    '9사단' : '20121290200',
    '11사단' : '20121790300',
    '12사단' : '20121490200',
    '15사단' : '20121390200',
    '17사단' : '20121190100',
    '20사단' : '20121790400',
    '21사단' : '20121490300',
    '22사단' : '20121890100',
    '23사단' : '20121890200',
    '25사단' : '20121290300',
    '27사단' : '20121390300',
    '28사단' : '20121690100',
    '30사단' : '20121290400',
    '31사단' : '20220280100',
    '32사단' : '20220280200',
    '35사단' : '20220280300',
    '36사단' : '20120180100',
    '37사단' : '20220280400',
    '39사단' : '20220280500',
    '50사단' : '20220280600',
    '51사단' : '20121190200',
    '53사단' : '20220280700',
    '55사단' : '20120180200',
    '육군훈련소' : '20020191700',
    '육군훈련소(23연대)' : '20020191800', # 육군훈련소 연대별 구분은 사라진 것 같습니다.
    '육군훈련소(25연대)' : '20020191900',
    '육군훈련소(26연대)' : '20020192000',
    '육군훈련소(27연대)' : '20020192100',
    '육군훈련소(28연대)' : '20020192200',
    '육군훈련소(29연대)' : '20020192300',
    '육군훈련소(30연대)' : '20020192400',
}

class Cookie:
    """the camp의 로그인 request에서 iuid와 token을 저장하는 모델입니다.
    """
    def __init__(self, r):
        """Cookie 모델을 만듭니다.

        :param r: requests.Response object
        :type r: requests.Response
        """
        try:
            cookie_header = r.headers['set-cookie']
            num_iuid = cookie_header.find('iuid=')
            num_token = cookie_header.find('Token=')
            self.iuid = cookie_header[num_iuid:num_iuid + 12]
            self.token = cookie_header[num_token:num_token + 36]
        except KeyError:
            self.iuid = None
            self.token = None

    def iuid(self):
        return self.iuid

    def token(self):
        return self.token


class Soldier:
    """훈련병의 정보를 저장하는 모델입니다.
    """
    def __init__(self, name, bday, enlist_date, unit):
        """Soldier 모델을 만듭니다.

        :param name: 훈련병의 이름
        :type name: str
        :param bday: 훈련병의 생년월일 ex) 19990812
        :type bday: int
        :param enlist_date: 훈련병의 입대일 ex)20200818
        :type enlist_date: int
        :param unit: 훈련병의 입대부대명(unit_codes 참고)
        :type unit: str
        """
        if unit not in unit_codes:
            raise exceptions.ThecampyValueError('해당 사단/육군훈련소 연대가 존재하지 않습니다.')

        unit_code = unit_codes[unit]

        self.name = name
        self.bday = bday
        self.enlist_date = enlist_date
        self.identity = "예비군인/훈련병"
        self.identity_code = '0000490001'
        self.army = '0000010001' #육군 코드
        self.unit = unit
        self.unit_code = unit_code

    def add_soldier_code(self, code):
        self.soldier_code = code

class Message:
    """훈련병에게 보낼 편지의 모델입니다.
    """
    def __init__(self, title, content):
        """Message 모델을 시작합니다.

        :param title: 편지의 제목입니다.
        :type title: str
        :param content: 편지의 내용입니다. (편지 내용은 1500자를 넘을 수 없습니다.)
        :type content: str
        """
        if len(content) > 1500:
            raise exceptions.ThecampyValueError("편지 내용이 1500자를 넘습니다.")
        self.title = title
        self.content = content

    @property
    def is_sent(self):
        return self._is_sent
    
    @is_sent.setter
    def is_sent(self, is_sent):
        if type(is_sent) is type(True):
            self._is_sent = is_sent
        else:
            raise exceptions.ThecampyValueError('is_sent must be bool')
    
    @is_sent.deleter
    def is_sent(self):
        del self._is_sent


class FileUploadResponse(NamedTuple):
    file_group_mgr_seq: str
    file_mgr_seq: str
    letter_file_group_mgr_seq: str