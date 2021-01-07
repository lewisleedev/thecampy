# thecampy - 더 캠프 파이썬 라이브러리


thecampy는 [parksb/the-camp-lib](https://github.com/parksb/the-camp-lib)을 참고하여 제작된 대국민 국군 소통 서비스 더 캠프의 파이썬 라이브러리입니다. 

 간단한 파이썬 코드 몇줄로 인터넷 편지를 보낼 수 있도록 구현되었습니다. 매일 [더 캠프 request code를 테스트합니다.](https://github.com/lewisleedev/thecampy/actions)

첫 파이썬 라이브러리다보니 부족한 부분이 많습니다. 오류사항은 Issue 부탁드립니다.

# Installation

  

    pip install thecampy

  

# Usage

  

    import thecampy

    my_soldier = thecampy.Soldier(

            [이름],

            [생일(yyyymmdd)],

            [입대일(yyyymmdd)],

            [부대(육군훈련소(30연대)],

    )

    msg = thecampy.Message([제목], [내용(1500자 이하)])

    tc = thecampy.client()

    tc.login(email, pw) #Prints 'Successfully Logged in'

    tc.add_soldier(my_soldier) #returns True

    tc.get_soldier(my_soldier) #returns soldier code

    tc.send_message(my_soldier, msg) #returns True

  
  

## 주의사항

- 더 캠프 계정은 이메일로 가입되어있어야 합니다. (카카오계정 지원 X)

- 부대이름을 정확히 입력해야합니다. ex) 육군훈련소(00연대), 7사단, 22사단...

- 인터넷편지는 '예비군인/훈련병'에게만 보낼 수 있습니다.

  

# Known Issues

- 테스트 전송시도 약 7번중 한번꼴로 resultCd=9019 (제목에 금지 문자가 들어있습니다) 오류가 발생했습니다.

  

# LICENSE

This project is licensed under the MIT License.
