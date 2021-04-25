# thecampy

thecampy는 [parksb/the-camp-lib](https://github.com/parksb/the-camp-lib)을 참고하여 제작된 대국민 국군 소통 서비스 더 캠프의 파이썬 라이브러리입니다.

입대 전, 훈련소에서 reddit 글들을 받아보고싶었는데, 파이썬으로는 보낼 수 있는 방법이 없어서 만들었습니다.

매 월요일 12시(UTC) [더 캠프 request code를 테스트합니다.](https://github.com/lewisleedev/thecampy/actions)

## Installation

    pip install thecampy

## Quick Start

    import thecampy

    my_soldier = thecampy.Soldier(

            [이름],

            [생일(yyyymmdd)],

            [입대일(yyyymmdd)],

    )

    msg = thecampy.Message([제목], [내용(1500자 이하)])

    tc = thecampy.client()

    tc.login(email, pw) #Prints 'Successfully Logged in'

    tc.get_soldier(my_soldier) #returns soldier code

    tc.send_message(my_soldier, msg) #returns True

## Before you use it

 - thecampy는 더캠프의 **이메일 계정**이 있어야합니다. 카카오계정은 지원하지 않습니다.
 - 더캠프의 인터넷편지는 육군 훈련병만 가능합니다.

## API

 See [API](api.md) for details.

## Changes

### v 2.0.0

- 부대코드 필수입력으로 변경([#7](https://github.com/lewisleedev/thecampy/issues/7) 참고)
- 버그 및 코드 수정