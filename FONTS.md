# 한글 폰트 조합 방법

본 리소스팩에 포함된 폰트는 아래의 기본 자형 데이터를 조합하여 11172글자의 현대 한글 음절을 생성하는 방법으로 제작되었습니다. 기본 자형 데이터에는 독립된 자소를 위한 글자 51개(자음 30자, 모음 21자)와, 초성용 글자 114개(19자x6벌), 중성용 글자 63개(21자x3벌), 종성용 글자 27개, 모두 합해서 총 255개의 글자가 포함되어 있습니다.

![base-bold](https://github.com/hseelab/mchanfont/blob/main/doc/base-bold.png?raw=true)
![base-regular](https://github.com/hseelab/mchanfont/blob/main/doc/base-regular.png?raw=true)

초성에는 1번부터 6번까지 총 6가지 변형이 있으며 각각의 변형은 다음 모음과 조합하기 위한 것입니다.

 * 1번, 4번: ㅏ, ㅐ, ㅑ, ㅒ, ㅓ, ㅔ, ㅕ, ㅖ, ㅣ
 * 2번, 5번: ㅘ, ㅙ, ㅚ, ㅝ, ㅞ, ㅟ, ㅢ
 * 3번, 6번: ㅗ, ㅛ, ㅜ, ㅠ, ㅡ

기본적으로 1, 2, 3번 변형은 받침이 없는 글자용, 4, 5, 6번 변형은 받침이 있는 글자용이지만, ㅜ, ㅝ, ㅞ, ㅟ, ㅠ와 조합되는 경우에는 받침이 없는 경우에도 4, 5, 6번 변형을 사용합니다.

중성은 총 3가지 변형이 있으며 각 변형은 다음의 경우 사용합니다.

 * 그룹 1: 받침이 없는 경우
 * 그룹 2: 받침 ㄴ과 조합되는 경우
 * 그룹 3: 기타 받침과 조합되는 경우

종성은 1가지 모양만 있지만, 다음 모음과 조합되는 경우에는 오른쪽으로 1 (얅은 글꼴) 또는 2 (두꺼운 글꼴) 픽셀 이동시켜 사용합니다.

 * 종성 이동: ㅐ, ㅒ, ㅔ, ㅖ, ㅙ, ㅞ

구체적인 코드는 bin/hfutil 파일에 포함된 composeChar() 함수를 참고하세요.

# 한글 폰트 조합 결과

아래 그림은 위에 설명된 알고리즘과 기본 자형 데이터를 사용하여 조합된 글자로 표시한 문장입니다.

![example-bold](https://github.com/hseelab/mchanfont/blob/main/doc/example-bold.png?raw=true)
![example-regular](https://github.com/hseelab/mchanfont/blob/main/doc/example-regular.png?raw=true)

한글 완성형에 포함된 2350개의 글자는 다음과 같으며, 아래 목록에 없는 나머지 글자도 모두 표현이 가능합니다.

![han2350-bold](https://github.com/hseelab/mchanfont/blob/main/doc/han2350-bold.png?raw=true)
![han2350-regular](https://github.com/hseelab/mchanfont/blob/main/doc/han2350-regular.png?raw=true)
