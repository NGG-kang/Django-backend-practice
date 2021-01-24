# Full-Stack-practice

기초부터 시작하는 풀스택 연습


 
### 1/20 django로 board 만들기 시작

### 1/23 django 유저 회원가입, 로그인, 로그아웃, 글 작성, 수정, 삭제 및 부트스트랩 

### 1/24 django 연습으로 이해한것 정리

django 기반으로 네비게이션 조차 없는 완전 기본 게시판을 만들어 봤다

만든 기능으로는

1. 회원가입
2. 로그인, 로그아웃
3. 게시글 등록
4. 게시글 보기
5. 게시글 수정
6. 게시글 삭제

볼품 없는 게시판이지만 연습한다는 의미로 만들어 보았다

------------

## 코드 정리

다음으로는 

게시판을 만들면서 사용한 코드와 내용들을 정리한 내용이다

기본적인 어드민 프로젝트 생성
  
    $ django-admin startproject project

만들어진 프로젝트에서

어드민 계정 생성

    $ python manage.py createsuperuser 

프로젝트에서 앱 생성

    $ python manage.py startapp app


이렇게 만들기만 해도 절반은 왔다

처음 시작 할 땐 세팅을 해줘야 하는데
project.setting 에서  INSTALLS_APPS에 app을 추가 해줘야 한다
이름이 app이라면 app.apps.AppConfig를 추가 하면 되는데 이건
app.setting.py에 들어있으므로 그것을 참조 하면 된다

