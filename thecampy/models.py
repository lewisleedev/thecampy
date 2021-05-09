from typing import NamedTuple

from thecampy import exceptions


class Cookie:
    def __init__(self, r):
        try:
            cookie_header = r.headers['set-cookie']
            num_iuid = cookie_header.find('iuid=')
            num_token = cookie_header.find('Token=')
            self.iuid = cookie_header[num_iuid:num_iuid + 12]
            self.token = cookie_header[num_token:num_token + 36]
        except KeyError:
            self.iuid = False
            self.token = False

    def iuid(self):
        return self.iuid

    def token(self):
        return self.token


class Soldier:
    def __init__(self, name, bday, enlist_date, unit):

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
            '육군훈련소' : '20020191700',
            '육군훈련소(23연대)' : '20020191800',
            '육군훈련소(25연대)' : '20020191900',
            '육군훈련소(26연대)' : '20020192000',
            '육군훈련소(27연대)' : '20020192100',
            '육군훈련소(28연대)' : '20020192200',
            '육군훈련소(29연대)' : '20020192300',
            '육군훈련소(30연대)' : '20020192400',
        }

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
    def __init__(self, title, content):
        self.title = title
        self.content = content


class FileUploadResponse(NamedTuple):
    file_group_mgr_seq: str
    file_mgr_seq: str
    letter_file_group_mgr_seq: str

