# Bulletin_Board_Service
MVP : 유저가 등급에 따라 게시글을 작성할 수 있는 서비스로 아래와 같은 기능을 제공합니다 <br>
- 유저의 등급 ; 관리자, 운영자, 일반사용자 <br>
- 게시판의 타입 ; 공지사항, 운영게시판, 자유게시판 <br>

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

</br>

## 💻 기술 스택
<div style='flex'>
<img src="https://img.shields.io/badge/Python3.9.5-3776AB?style=for-the-badge&logo=Python&logoColor=white" >
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=PostgreSQL&logoColor=white">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white">
	<img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=for-the-badge&logo=Amazon EC2&logoColor=white">
	<img src="https://img.shields.io/badge/Amazon RDS-527FFF?style=for-the-badge&logo=Amazon RDS&logoColor=white">
</div>

## 👨‍👩‍👧 작업 구성원과 역할분담

<details>
<summary>	&nbsp	<a href="https://khw7876.tistory.com/"> 고현우 </a>	</summary>  

- 통계 기능 : 남여별
- simpleJWT 로그인 기능 구현
- 게시글 서비스 service layer 분리
- 게시글 서비스 DRUD 기능 구현
- 게시글 서비스 테스트 케이스 작성
- permission 리팩토링
- permission 테스트 케이스 작성
</details>


<details>
<summary>	&nbsp	<a href="https://velog.io/@kimphysicsman"> 김동우 </a>	</summary>  

- 통계 기능 : 나이별, 접속시간별
- 회원가입 기능 구현
- 사용자 정보 수정 기능 구현
- 회원탈퇴 기능 구현
- 유저 서비스 service layer 분리
- 유저 서비스 모델링
- 유저 서비스 테스트 케이스 작성
</details>


<details>
<summary>	&nbsp	<a href="https://nicesugi.tistory.com/"> 윤슬기 </a>	</summary>  

- 게시글 서비스 앱 모델링
- 게시글 서비스 DRUD 리팩토링 
- EC2 배포 작업
- RDS  데이터베이스 배포 작업
- 도메인 연결
- https 설정
- 배포 관련 빌드 파일 수정 작업
</details>


<details>
<summary>	&nbsp	<a href="https://velog.io/@tasha_han_1234"> 한예슬 </a>	</summary>  

- permission 작업
- permission 리팩토링
- permission 테스트 케이스 작성
- 배포 빌드 작업
    - nginx.conf 작성
    - docker-compose.yml 작성
    - Dockerfile 작성
    - static 설정
- EC2 배포 작업
- RDS 데이터베이스 배포 작업
</details>

</br>

## 👉 ERD
<img width="785" alt="스크린샷 2022-09-01 오후 10 44 18" src="https://user-images.githubusercontent.com/104303285/187929462-fdf80dd7-388c-414d-9b85-7a5371704ab1.png">
</br>

## 🙏 API 명세서
<img width="912" alt="스크린샷 2022-09-06 오전 9 51 46" src="https://user-images.githubusercontent.com/104303285/188525114-30e4e9d0-0d01-4c83-802a-7874c6836e69.png">
</br>

## 🙏 REQUEST 도큐먼트 (사진누르면 도큐먼트로 이동!)
<a href="https://documenter.getpostman.com/view/20981400/VV4ryJhH"> <img width="255" alt="스크린샷 2022-09-06 오후 3 18 13" src="https://user-images.githubusercontent.com/104303285/188560698-e19adce6-b035-4364-9330-21ef83e0aaba.png"></a>

</br>
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

### ❓ Lint
- autopep8 사용
- github actions 작동시 lint with flake8적용

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

### 📝 Unit Test
- Service Layer 구축
- Service 에 대하여 예측가능한 Error를 Unittest진행
- 결과가 나온 Error들을 Try, Execpt를 통한 핸들링
- API에 대한 Unittest에서 제대로 Error에 대한 핸들링이 이루어 졌는가를 확인

</br>
</br>

## 🎇 배포 이미지
<img width="963" alt="b1" src="https://user-images.githubusercontent.com/104303285/188524821-a964f346-ecfa-4240-966e-7d40d6a0253b.png">



## 💻 트러블슈팅
### ***문제 1. Ubuntu 환경에서 nginx컨테이너가 계속 꺼지는 현상이 발생 같은 문제로 IP주소가 로컬주소로 연결되기도 하였음***
- 원인 : 
    - nginx.conf 작성시 문법이 틀렸고 프록시패스도 정확하지 않게 설정되어 있었음. 
    - listen:80 에서 ':' 을 사용하였던 점. 
    - 프록시 패스에 upstream을 사용해 불러왔는데, 불러온 이름을 사용하지도 않았고 문법 자체도 오류가 있었음.
- 해결 : 
    - docker-compose up 하여 로그를 확인해가며 어느 구간에서 오류가 발생했는지 확인 listen 80 으로 바꿔줌 
    - upstream 을 삭제해주고 프록시패스를 http://app:8000 으로 직접적으로 설정함


### ***문제 2. 접근 권한을 로직을 작성하여서 만들다보니, 매번 로직을 해석을 해야한다는 문제점이 있었음***
- 원인 : 
    - 함수를 타고 들어갈 때 마다, 쿼리를 접속하는 로직이 있었음 이게 어떤 역할을 하는 로직인지를 볼 때마다 파악을 해야 했음
- 해결 : 
    - 같은 로직을 함수로 대체하였고, 함수 이름을 어떠한 로직인지에 대한 설명으로 대체를 하였음


### ***문제 3. 작업시에 통일성이 없는 습관들이 반영된 코드들이 있었음. 예를 들어 class 사이에 어떤 줄은 enter키가 한번, 어떤 줄은 두번 같은 상황 발생***
- 원인 : 
    - 사전에 팀의 작업방식을 몰랐기에 발생
- 해결 : 
    - 팀원의 의견을 반영하여 최대한 깔끔한 작업물을 내기 위하여 노력
    
    
### ***문제 4.  RDS 데이터베이스 연결이 되질 않음***
- 원인 : 
    - EC2 인스턴스의 보안그룹 미설정
- 해결 : 
    - RDS 생성시 엔진에 맞는 포트를 EC2 인스턴스에 보안그룹을 설정해주어 연결 완료.
    - 인바운드규칙 5432 Postgre 설정.



