# thecampy - 더 캠프 파이썬 라이브러리

thecampy는 [parksb/the-camp-lib](https://github.com/parksb/the-camp-lib)을 참고하여 제작된 대국민 국군 소통 서비스 더 캠프의 파이썬 라이브러리입니다. 간단한 파이썬 코드 몇줄로 인터넷 편지를 보낼 수 있도록 구현되었습니다.


# Installation

    pip install thecampy

# Usage

    import thecampy
    
    soldier = thecampy.Soldier(
			    [이름],
				[생일(yyyymmdd)],
				[입대일(yyyymmdd)],
				[신분(예비군인/훈련병)],
				[부대(육군훈련소(30연대)],
				[관계코드]
				)
	msg = thecampy.Message([제목], [내용(1500자 이하)])
	
	thecampy = thecampy.Client()
	thecampy.login(emain, pw) #Prints 'Successfully Logged in'
	thecampy.add_soldier(soldier) #returns True
	thecampy.get_soldier(soldier) #returns soldier code
	thecampy.send_message(soldier, msg) #returns True

## 주의사항

 - 더 캠프 계정은 이메일로 가입되어있어야 합니다. (카카오계정 지원 X)
 - 부대이름을 정확히 입력해야합니다. ex) 육군훈련소(00연대), 7사단, 22사단...
 - 인터넷편지는 '예비군인/훈련병'에게만 보낼 수 있습니다.

# Known Issues
 - 테스트 전송시도 약 7번중 한번꼴로 resultCd=9019 (제목에 금지 문자가 들어있습니다) 오류가 발생했습니다. 재시도하면 정상 발송되지만, 오류 파악중에 있습니다.

# Models
추가중

# LICENSE
This project is licensed under the MIT License.
