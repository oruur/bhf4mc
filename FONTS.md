# 한글 폰트 조합 방법

리소스팩에 포함된 폰트는 초/중/종성 각각 6/3/1벌의 기본 자형을 조합하여
11,172글자의 한글 음절을 생성하는 방법으로 제작되었습니다. 기본 자형 데이터에는
독립된 자소를 위한 글자 51개 (자음 30자 + 모음 21자)와, 초성용 글자 114개 (19자
x 6벌), 중성용 글자 63개 (21자 x 3벌), 종성용 글자 27개, 모두 합해서 총 255개의
글자가 포함되어 있습니다.

![base-bold](https://github.com/hseelab/mchanfont/blob/main/images/base-bold.png?raw=true)
![base-regular](https://github.com/hseelab/mchanfont/blob/main/images/base-regular.png?raw=true)

초성에는 1번부터 6번까지 총 6가지 모양이 있으며 각각의 모양은 다음 모음과
조합될 때 사용됩니다. 기본적으로 1, 2, 3번 모양은 받침이 없는 글자용, 4, 5, 6번
모양은 받침이 있는 글자용이지만, ㅜ, ㅝ, ㅞ, ㅟ, ㅠ 와 조합되는 경우에는 받침이
없는 경우에도 4, 5, 6번 모양이 사용됩니다.

 * 1번, 4번: ㅏ, ㅐ, ㅑ, ㅒ, ㅓ, ㅔ, ㅕ, ㅖ, ㅣ
 * 2번, 5번: ㅘ, ㅙ, ㅚ, ㅝ, ㅞ, ㅟ, ㅢ
 * 3번, 6번: ㅗ, ㅛ, ㅜ, ㅠ, ㅡ

중성은 총 3가지 모양이 있으며 각 모양은 다음의 경우 사용됩니다.

 * 1번: 받침이 없는 경우
 * 2번: 받침 ㄴ과 조합되는 경우
 * 3번: 기타 받침과 조합되는 경우

종성은 1가지 모양만 있지만, 다음 모음과 조합되는 경우에는 오른쪽으로 1픽셀
이동하여 조합됩니다.

 * 종성 이동: ㅐ, ㅒ, ㅔ, ㅖ, ㅙ, ㅞ

구체적인 코드는 util/hfutil.py 파일에 포함된 composeChar() 함수를 참고하세요.

# 한글 폰트 조합 결과

아래 그림은 위에 설명된 알고리즘과 기본 자형 데이터를 사용하여 조합된 글자로
표시한 문장입니다.

![example-bold](https://github.com/hseelab/mchanfont/blob/main/images/example-bold.png?raw=true)
![example-regular](https://github.com/hseelab/mchanfont/blob/main/images/example-regular.png?raw=true)

다음은 모든 가능한 [초성 + 중성] 및 [중성 + 종성] 조합의 확인이 가능한 1,764
(= 19 x 21 x 3 + 21 x 27) 글자를 표시한 것입니다.

![han1764-bold](https://github.com/hseelab/mchanfont/blob/main/images/han1764-bold.png?raw=true)
![han1764-regular](https://github.com/hseelab/mchanfont/blob/main/images/han1764-regular.png?raw=true)

한국어에서 자주 사용되는 2,350 글자는 다음과 같으며, 목록에 없는 나머지 글자도
모두 표현 가능합니다.

![han2350-bold](https://github.com/hseelab/mchanfont/blob/main/images/han2350-bold.png?raw=true)
![han2350-regular](https://github.com/hseelab/mchanfont/blob/main/images/han2350-regular.png?raw=true)
