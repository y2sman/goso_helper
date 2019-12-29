# goso_helper

## 참고
[추가적인 설명이 있는 블로그](https://y2sman.github.io/2019/12/30/2019_12_30/)

## 설치
python3 에서 작동합니다.

    pip install requests
    pip install beautifulsoup4
    pip install pdfkit
    pip install urllib3

위의 패키지가 필요합니다.

추가적으로 pdfkit을 사용하기 위해, https://wkhtmltopdf.org/ 이 필요합니다. 윈도우 기준으로 기본 옵션으로 설치했을 경우 그냥 작동합니다. 타 OS의 경우 pdfkit의 config에서 wkhtmltopdf의 경로를 변경해야 작동합니다.

## How to Use
대상 갤러리의 주소가 필요합니다.

    https://gall.dcinside.com/board/view/?id=iu_new&no=4799774&page=1

아무 글이나 클릭해 위와 같은 주소를 가져옵니다.

    https://gall.dcinside.com/board/view/?id=iu_new&no=

no= 다음 내용을 지우고 target_URL 변수에 입력해주세요. 글 번호는 사이트에서 확인할 수 있습니다.

## Match_str

대상 게시글의 제목과 본문에 포함되어야할 키워드를 입력해주세요. 하나라도 있으면 저장합니다.
