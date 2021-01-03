import requests

def test_login():
    r = requests.post(
        url = 'https://www.thecamp.or.kr/login/loginA.do',
        json = True,
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

    assert r.status_code == requests.codes.ok

def test_add_solider():
    r = requests.post(
        url = 'https://www.thecamp.or.kr/missSoldier/insertDirectMissSoldierA.do',
        json = True,
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    
    assert r.status_code == requests.codes.ok

def test_get_soldier():
    r = requests.post(
        url = 'https://www.thecamp.or.kr/main/cafeCreateCheckA.do',
        json = True,
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

    assert r.status_code == requests.codes.ok

def test_send_message():
    r = requests.post(
        url = 'https://thecamp.or.kr/consolLetter/insertConsolLetterA.do?',
        json = True,
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    print(r.status_code)
    assert r.status_code == requests.codes.ok