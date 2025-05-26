// http://beemarketer.co.kr/bookreview/one-page-proposal/
// one page proposal을 참고해서 작성함.

#set text(
  font: "Pretendard",
)
#show math.equation: set text(font: "STIX Two Math")
#set quote(block: true)
#show link: set text(fill: blue)


= Py Review App Proposal
소속 : 정보컴퓨터공학부 인공지능전공 \
이름 : 최재원 (2025)

#line(length: 100%, stroke: 0.35pt)

=== 제목 및 부제
*Py Review App* (파이썬 코드 리뷰 ai + linter, formatter 를 제공하는 웹앱)

=== 동기 및 목표
실력을 올리는데는 가장 중요한 요소 중 하나는 빠른 피드백이다. 동기들과 파이썬 스터디를 진행하고 있는데 내가 하나하나 피드백 해주기에는 물리적 시간이 부족하다는 것을 깨닫고 이를 ai를 통해 해결할 수 있겠다는 생각이 들었다. 또한 neoESPA처럼 linter, formatter 기능을 가지고도 있으면 좋을 것 같았다. 따라서 이러한 기능을 가진 python code review 웹앱을 만들어볼려고 한다.

=== 하위 목표

- linter
- formatter
- ai review with OpenAI API

=== 논리적 근거
무언가를 제대로 빠르게 배우는 방법은 의식적인 연습을 하는 것입니다. 특히 이러한 의식적인 연습의 중요한 요소는 빠른 피드백입니다. 특히 최근 ai 기술을 이용한다면 이러한 피드백을 받음으로써 실력을 향상시킬 수 있을꺼라고 생각합니다.

#quote(attribution: [#link("https://en.wikipedia.org/wiki/Practice_(learning_method)#Characteristics_of_deliberate_practice", "From: Characteristics of deliberate practice - Wikipedia")])[
The student should be able to access immediate feedback about his performance, so they can make the changes needed to improve. ]

=== 필요 자원
- web app : 10시간
  - 로그인 기능 : 4시간
  - 프론트 엔드 기능들 (에디터) : 4시간
- ai review : 5시간

최소 24시간 \~ 최대 48시간 필요

=== 현재 상태
제안서를 작성하고 #link("https://github.com/cjaewon/pyreview-app", "github repo")를 만듬. \


=== 구현 계획

- login => session을 사용하여 구현한다.
- frontend => editor 라이브러리와 htmx를 사용한다
  - 리액트 같은 라이브러리를 사용하는 것은 너무 무겁다.
  - htmx이 사용하기 힘들면 AlpineJS와 같은 간단한 반응형 라이브러리를 사용한다.
- linter, formatter => rust로 작성된 고성능 linter, formatter인 ruff를 사용하여 구현한다.
- ai review => openAI의 o4-mini api를 사용한다.
- database => 만약 쓰게된다면 sqlite3을 사용한다.
