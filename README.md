![PyPI](https://img.shields.io/pypi/v/thecampy?style=for-the-badge)![GitHub](https://img.shields.io/github/license/lewisleedev/thecampy?style=for-the-badge)![GitHub Workflow Status](https://img.shields.io/github/workflow/status/lewisleedev/thecampy/%EB%8D%94%EC%BA%A0%ED%94%84%20response%20%ED%99%95%EC%9D%B8?label=Response&style=for-the-badge)

# thecampy - 더 캠프 파이썬 라이브러리


thecampy는 [parksb/the-camp-lib](https://github.com/parksb/the-camp-lib)을 참고하여 제작된 대국민 국군 소통 서비스 더 캠프의 파이썬 라이브러리입니다. 

 파이썬으로 인터넷 편지를 보낼 수 있도록 구현되었습니다. 매 월요일 12시(UTC) [더 캠프 request code를 테스트합니다.](https://github.com/lewisleedev/thecampy/actions)

첫 파이썬 라이브러리다보니 부족한 부분이 많습니다. 오류사항은 Issue 부탁드립니다.

# Installation

  
    pip install thecampy

  

# Quickstart

  

    import thecampy

    my_soldier = thecampy.Soldier(

            [이름],

            [생일(yyyymmdd)],

            [입대일(yyyymmdd)],

            [부대명(ex: 육군훈련소)],

    )

    msg = thecampy.Message([제목], [내용(1500자 이하)])

    image = thecampy.ThecampyImage('sample.png')

    tc = thecampy.client()

    tc.login(email, pw) #Prints 'Successfully Logged in'

    tc.get_soldier(my_soldier) #returns soldier code

    tc.send_message(my_soldier, msg, image) #returns True

자세한 사항은 [프로젝트 홈페이지](https://dev.lewislee.net/thecampy)에서 확인할 수 있습니다.

# LICENSE

This project is licensed under the MIT License.