# thecampy

thecampy는 [parksb/the-camp-lib](https://github.com/parksb/the-camp-lib)을 참고하여 제작된 대국민 국군 소통 서비스 더 캠프의 파이썬 라이브러리입니다.

입대 전, 훈련소에서 reddit 글들을 받아보고싶었는데, 파이썬으로는 보낼 수 있는 방법이 없어서 만들었습니다.

매 월요일 12시(UTC) [더 캠프 request code를 테스트합니다.](https://github.com/lewisleedev/thecampy/actions)

## Installation

thecampy는 pip으로 설치할 수 있습니다. 

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

## Example
    import thecampy

    my_soldier = thecampy.Soldier('홍길동',20010101,20210225, '육군훈련소')

    msg = thecampy.Message('제목', '내용')

    tc = thecampy.client()

    tc.login('test@naver.com', 'test1234@password!')

    tc.get_soldier(my_soldier)

    tc.send_message(my_soldier, msg)

## Before you use it

 - thecampy는 더캠프의 **이메일 계정**이 있어야합니다. 카카오계정은 지원하지 않습니다.
 - 더캠프의 인터넷편지는 육군 훈련병만 가능합니다.

## 부대명과 부대코드

부대명을 정확히 입력해야 인터넷 편지를 보낼 수 있습니다. 부대명 목록과 상응하는 부대코드는 다음과 같습니다.

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

## Changes

### v 2.0.0

- 부대코드 필수입력으로 변경([#7](https://github.com/lewisleedev/thecampy/issues/7) 참고)
- 버그 및 코드 수정