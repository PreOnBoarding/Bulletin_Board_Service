# Wayne_Hills_Ventures 기업과제

## 👨‍👩‍👧 작업 구성원
- [고현우](https://khw7876.tistory.com/)
- [김동우](https://velog.io/@kimphysicsman)
- [윤슬기](https://nicesugi.tistory.com/)
- [한예슬](https://velog.io/@tasha_han_1234)

## 📜 과제 분석

- 서비스 정의
  - MVP 서비스 : 유저가 게시판을 이용 <br>
- User 등급 존재 (ex - 관리자, 운영자, 일반사용자) <br>
- Post 타입 존재 (공지사항, 운영게시판, 자유게시판) <br>

  <details>
  <summary>공지 게시판</summary>
  <div markdown="1">
    - 조회 : 모두에게 <br>
    - 작성 : 운영자 <br>
    - 수정 : 운영자 <br>
    - 삭제 : 운영자 <br>
  </div>
  </details>
  <details>
  <summary>운영 게시판</summary>
  <div markdown="1">
    - 조회 : 운영자 <br>
    - 작성 : 운영자 <br>
    - 수정 : 작성 운영자 <br>
    - 삭제 : 작성 운영자 <br>
  </div>
  </details>
  <details>
  <summary>자유 게시판</summary>
  <div markdown="1">
    - 조회 : 모두에게 <br>
    - 작성 : 가입이 된 사람 <br>
    - 수정 : 작성자 <br>
    - 삭제 : 작성자, 운영자 <br>
  </div>
  </details>
- 통계 기능 (남/여,  나이별, 접속시간별 ⇒ 유저 모델에 포함)

## 👉 ERD
<img width="785" alt="스크린샷 2022-09-01 오후 10 44 18" src="https://user-images.githubusercontent.com/104303285/187929462-fdf80dd7-388c-414d-9b85-7a5371704ab1.png">
</br>

## 📌 컨벤션
### ❓ Commit Message
- feat/ : 새로운 기능 추가/수정/삭제
- enhan/ : 기존 코드에 기능을 추가하거나 기능을 강화할 때
- refac/ : 코드 리팩토링,버그 수정
- test/ : 테스트 코드/기능 추가
- edit/ : 파일을 수정한 경우(파일위치변경, 파일이름 변경, 삭제)

### ❓ Naming
- Class : Pascal 
- Variable : Snake 
- Function : Snake 
- Constant : Pascal + Snake

### ❓ 주석
- Docstring을 활용하여 클래스와 함수단위에 설명을 적어주도록 하자.
- input/output을 명시하여 문서 없이 코드만으로 어떠한 결과가 나오는지 알 수 있도록 하자.

### 🚷 벼락치기의 규칙
- 컨벤션 지키기
- Commit 단위 지키기
- PR을 올리고 conflict가 발생했다면 모두에게 상황을 알리고 Pull 받도록 권고
- 말 한마디의 가치를 알고 신중하게 내뱉기
- 문제를 마주하여 트러블을 겪었다면, 어떻게 해결을 했는지 공유를 해주기
- 각자의 작업을 미리 작성을 하여서 각자의 작업을 공유하기
- 각자 맡은 기능의 브랜치에서 작업을 하며 PR을 올린다. PR은 본인 이외의 2인 이상에게 승인을 받아야 merge 가능
### 🆕<new 규칙>
- 9AM 모여서 각자의 할일 리스트 작성
- 4PM 모여서 아침에 계획했던 결과확인, PR일괄 확인 및 작업내용 공유
- 9PM TIL 링크 공유 및 하루의 마무리
- PR 일괄 확인시에는 어떠한 작업에 대한 PR인지 간단한 설명 후 다른 팀원의 검토 진행

### 📝 UniTest
- Service Layer 구축
- Service 에 대하여 예측가능한 Error를 Unitest진행
- 결과가 나온 Error들을 Try, Execpt를 통한 핸들링
- API에 대한 Unitest에서 제대로 Error에 대한 핸들링이 이루어 졌는가를 확인


