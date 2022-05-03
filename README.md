![PyPI](https://img.shields.io/pypi/v/thecampy?style=for-the-badge)![GitHub](https://img.shields.io/github/license/lewisleedev/thecampy?style=for-the-badge)![GitHub Workflow Status](https://img.shields.io/github/workflow/status/lewisleedev/thecampy/%EB%8D%94%EC%BA%A0%ED%94%84%20response%20%ED%99%95%EC%9D%B8?label=Response&style=for-the-badge)

> :warning: 현재 더캠프 내부 시스템의 변화로 기존 v3.0.2는 작동하지 않습니다. 4.0.0a 버젼은 beautifulsoup을 사용해 soldier_code를 받아옵니다. 카페 가입을 수동으로 해주어야합니다.

# thecampy - 더캠프 파이썬 라이브러리

thecampy는 [parksb/the-camp-lib](https://github.com/parksb/the-camp-lib)을 참고하여 제작된 대국민 국군 소통 서비스 더 캠프의 파이썬 라이브러리입니다. 

파이썬으로 인터넷 편지를 보낼 수 있도록 구현되었습니다. 매 월요일 12시(UTC) [더 캠프 request code를 테스트합니다.](https://github.com/lewisleedev/thecampy/actions)

## Description

thecampy는 [parksb/the-camp-lib](https://github.com/parksb/the-camp-lib)을 참고하여 제작되어 더캠프 인터넷 편지를 간단하게 보낼 수 있도록 만들어진 파이썬 라이브러리입니다.

## Getting Started

### Before you start

* **내부 시스템의 변화로, v4.0.0a부터 훈련병 카페 가입을 실행 전 수동으로 미리 해주셔야합니다.**

### Dependencies

* requests
* bs4

### Installing

* `pip install thecampy`

### Quickstart

```
import thecampy

my_soldier = thecampy.Soldier('이름')
msg = thecampy.Message('test', 'test')

tc = thecampy.Client(email, pw)
tc.get_soldier(my_soldier) # returns soldier_code
tc.send_message(my_soldier, msg)
```

## Disclaimer

thecampy는 더캠프의 서비스업자와 관련이 없습니다. thecampy는 더캠프 서비스를 악용하는데에 사용할 수 없습니다. **thecampy의 사용으로인한 책임은 전적으로 사용자에게 있습니다.**

## Contributors

[lewisleedev](https://github.com/lewisleedev)

[2minchul](https://github.com/2minchul)

[OneTop4458](https://github.com/OneTop4458)

[SyphonArch](https://github.com/SyphonArch)

[leesangwon](https://github.com/leeesangwon)

## Version History

- 4.0.0a
    - **더 캠프 시스템 상 변화에 따른 작동방법 수정**
        - 개발 초기단계로, 버그 리포트 부탁드립니다.

- 3.0.2
    - `__init__`함수가 None이 아닌 값을 가지던 버그 수정 #10 (by [leesangwon](https://github.com/leeesangwon))

- 3.0.1
    - 55사단(용인) 부대코드 추가 (이메일 제안)
    - `__init__.py`와 `README.md`에서 Client가 소문자로 시작하던 오류 수정

- 3.0.0
    - login method 삭제 및 __init__으로 이전
    - docstring 추가
    - and lot more fixes, chores and refactors

## License

This project is licensed under the MIT License - see the LICENSE file for details
