import requests
from thecampy import utils, models, exceptions

class client:
    def enforce_login(self):
        if not hasattr(self, 'cookie'):
            raise ValueError("로그인이 필요합니다.")

    def login(self, id, password):

        form = {
            "state": 'email-login',
            "autoLoginYn": 'N',
            "userId": id,
            "userPwd": password,
        }

        r = requests.post(
            url= utils.request_url('login/loginA.do'),
            json = True,
            data = form,
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            },
        )
        
        if (r.status_code != requests.codes.ok):
            raise exceptions.ThecampyReqError('HTTP 에러: {}'.format(r.status_code))

        self.cookie = models.Cookie(r)

        if (self.cookie.iuid == False or self.cookie.token == False):
            raise exceptions.ThecampyException('알 수 없는 에러 {}'.format(r.json()))
        else:
            print('Successfully logged in.')

        return {
            'iuid' : self.cookie.iuid,
            'token' : self.cookie.token
        }
    
    def add_soldier(self, soldier):
        self.enforce_login()
        form = {
            "missSoldierClassCdNm": soldier.identity, #성분 반환 (예비군인/훈련병)
            "grpCdNm": '육군',
            "missSoldierClassCd": soldier.identity_code,
            "grpCd": '0000010001',#육군
            "name": soldier.name,
            "birth" : soldier.bday,
            "enterDate" : soldier.enlist_date,
        }

        r = requests.post(
            url = utils.request_url('missSoldier/insertDirectMissSoldierA.do'),
            json = True,
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie' : "{}; {}".format(self.cookie.iuid, self.cookie.token)
            },
            data = form
        )
        
        if (r.status_code != requests.codes.ok):
            raise exceptions.ThecampyReqError('HTTP 에러: {}'.format(r.status_code))

        ok_resultCd = ['0000', 'E001']

        if (r.json()['resultCd'] not in ok_resultCd):
            raise exceptions.ThecampyException("알 수 없는 에러: resultCd: {}".format((r.json()['resultCd'])))

        return True

    def get_soldier(self, soldier):
        self.enforce_login()
        form = {
            "name" : soldier.name,
            "birth" : soldier.bday,
            "enterDate" : soldier.enlist_date
        }
        
        r = requests.post(
            url = utils.request_url('main/cafeCreateCheckA.do'),
            json = True,
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie' : "{}; {}".format(self.cookie.iuid, self.cookie.token)
            },
            data = form
        )
        
        if (r.status_code != requests.codes.ok):
            raise exceptions.ThecampyReqError('HTTP 에러: {}'.format(r.status_code))
        
        if not r.json():
            raise exceptions.ThecampyReqError('응답값이 없습니다.')

        if len(r.json()['listResult']) == 0:
             raise exceptions.ThecampyValueError("해당하는 훈련병을 찾을 수 없습니다.")
        
        if r.status_code == 200 and r.json()["resultCd"] != '9999':
            raise exceptions.ThecampyException("알 수 없는 오류")

        self.soldier_code = r.json()['listResult'][0]['traineeMgrSeq']
        
        soldier.add_soldier_code(self.soldier_code)

        return self.soldier_code
    
    def send_message(self, soldier, message):
        if soldier.identity != '예비군인/훈련병':
            raise exceptions.ThecampyValueError('예비군인/훈련병에게만 편지를 보낼 수 있습니다.')
        
        if not soldier.soldier_code:
            raise exceptions.ThecampyValueError('훈련병 식별코드를 받지 못하였습니다.')

        form = {
            'traineeMgrSeq' : soldier.soldier_code,
            'sympathyLetterContent': message.content,
            'sympathyLetterSubject': message.title,
            'boardDiv': 'sympathyLetter',
            'tempSaveYn': 'N',
        }

        r = requests.post(
            url = utils.request_url('consolLetter/insertConsolLetterA.do?'),
            json = True,
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie' : "{}; {}".format(self.cookie.iuid, self.cookie.token)
            },
            data = form
        )

            
        if r.status_code == 200 and r.json()["resultCd"] == '9019':
            raise exceptions.ThecampyException("9019")
        elif r.json()["resultCd"] != '0000':
            raise exceptions.ThecampyException("알 수 없는 오류: resultCd={}".format(r.json()["resultCd"]))

        if (not r.json()):
            raise exceptions.ThecampyReqError('응답값이 없습니다.')

        return True