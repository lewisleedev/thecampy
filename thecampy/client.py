from typing import Optional

import requests

from thecampy import exceptions, images, models, utils


class client:
    upload_url_api_key = 'xIerQL8gDg4qKd5sbVjAr7rgzf2FtJ6C4OKgTv25'
    upload_api_key = 'b3JedGhtQo5RFOR2pBpN6amkfAMJTZUY7tosboGt'

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
            "enterDate" : soldier.enlist_date,
            "trainUnitCd": soldier.unit_code,
            "grpCd": '0000010001'
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
        
        if r.status_code == 200 and r.json()["resultCd"] != '9999':
            raise exceptions.ThecampyException('알 수 없는 오류: {}'.format(r.json()))

        if len(r.json()['listResult']) == 0:
             raise exceptions.ThecampyValueError("해당하는 훈련병을 찾을 수 없습니다.")

        self.soldier_code = r.json()['listResult'][0]['traineeMgrSeq']
        
        soldier.add_soldier_code(self.soldier_code)

        return self.soldier_code

    def send_message(self, soldier: models.Soldier, message: models.Message,
                     image: Optional[images.ThecampyImage] = None):
        if soldier.identity != '예비군인/훈련병':
            raise exceptions.ThecampyValueError('예비군인/훈련병에게만 편지를 보낼 수 있습니다.')

        if not soldier.soldier_code:
            raise exceptions.ThecampyValueError('훈련병 식별코드를 받지 못하였습니다.')

        form = {
            'traineeMgrSeq': soldier.soldier_code,
            'sympathyLetterContent': message.content,
            'sympathyLetterSubject': message.title,
            'boardDiv': 'sympathyLetter',
            'tempSaveYn': 'N',
        }

        if image:
            upload_response = self._upload_image(image)
            form['sympathyLetterEditorFileGroupSeq'] = upload_response.letter_file_group_mgr_seq
            form['fileGroupMgrSeq'] = upload_response.file_group_mgr_seq
            form['fileMgrSeq'] = upload_response.file_mgr_seq

        r = requests.post(
            url=utils.request_url('consolLetter/insertConsolLetterA.do?'),
            json=True,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': "{}; {}".format(self.cookie.iuid, self.cookie.token)
            },
            data=form
        )

        if r.status_code == 200 and r.json()["resultCd"] == '9019':
            raise exceptions.ThecampyException("9019")
        elif r.json()["resultCd"] != '0000':
            raise exceptions.ThecampyException("알 수 없는 오류: resultCd={}".format(r.json()["resultCd"]))
        if (not r.json()):
            raise exceptions.ThecampyReqError('응답값이 없습니다.')

        return True

    def _get_upload_url(self, image: images.ThecampyImage) -> str:
        r = requests.post(
            url='https://private-api.thecamp.or.kr/upload/TC-GetUploadURL?s=prd',
            json=[{
                "path": image.path,
                "t": 100,
                "ct": image.ct,
            }],
            headers={
                'x-api-key': self.upload_url_api_key,
            },
        )
        response_data: list = r.json()
        if not response_data:
            raise exceptions.ThecampyReqError('응답값이 없습니다.')
        if not (response_data[0] or response_data[0].get('url')):
            raise exceptions.ThecampyReqError('응답값이 올바르지 않습니다.')
        upload_url = response_data[0]['url']
        return upload_url

    def _upload_cdn(self, image: images.ThecampyImage):

        upload_url = self._get_upload_url(image)

        with image as f:
            r = requests.put(
                url=upload_url,
                data=f,
                headers={
                    'x-api-key': self.upload_api_key,
                }
            )
        if r.status_code != 200:
            raise exceptions.ThecampyReqError('이미지 업로드에 실패하였습니다.')

    def _upload_image(self, image: images.ThecampyImage) -> models.FileUploadResponse:
        self._upload_cdn(image)

        form = {
            'boardDiv': 'sympathyLetter',
            'savedFileNm': image.saved_file_name,
            'filePath': image.file_path,
            'oriFileNm': 'upload',
            'extNm': image.metadata.type.lower(),
            'fileSize': str(image.metadata.file_size),
            'imgWSize': str(image.metadata.width),
            'imgHSize': str(image.metadata.height),
            'fileType': 'image',
        }
        r = requests.post(
            url=utils.request_url('commonFileUploadCdn.do'),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': "{}; {}".format(self.cookie.iuid, self.cookie.token)
            },
            data=form,
        )
        response_data: dict = r.json()
        if not response_data:
            raise exceptions.ThecampyReqError('응답값이 없습니다.')
        result_code = response_data.get('resultCd')

        if r.status_code == 200 and result_code == '9019':
            raise exceptions.ThecampyException("9019")
        elif result_code != '0000':
            raise exceptions.ThecampyException(f"알 수 없는 오류: resultCd={result_code}")

        try:
            return models.FileUploadResponse(
                file_group_mgr_seq=response_data['fileGroupMgrSeq'],
                file_mgr_seq=response_data['fileMgrSeq'],
                letter_file_group_mgr_seq=response_data['fileList'][0]['sympathyLetterFileGroupMgrSeq'],
            )
        except KeyError:
            raise exceptions.ThecampyReqError('응답값이 올바르지 않습니다.') from None
