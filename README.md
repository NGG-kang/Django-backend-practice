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

### 1. 프로젝트 및 앱 생성

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

이름이 app이라면 app.apps.AppConfig를 추가 하면 되는데

app.setting.py에 들어있으므로 그것을 참조 하면 된다


### 2. 모델 수정(데이터베이스 생성)

django에서는 데이터베이스 생성 명령어를 지원한다

생성한 app의 models에서 클래스를 만들면

django의 명령어 하나만으로 sqlite3 데이터베이스를 뚝딱 만들어준다

거기다 sql문 쓸 일도 없으니 얼마나 편한가?

일단 본 프로젝트에 사용한 model을 올려보자면

```python
class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    context = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```

대충 Board 클래스로 만들고

title, conext, pub_date를 넣었다, id는 자동으로 만들어줘서 따로 만들 필요는 없다.

django에서는 db를 models로 말한다

CharField, DateTimeField 만 사용했다

django의 Field들은 
[DjangoDoc](https://docs.djangoproject.com/en/3.1/ref/models/fields/)
 사이트에 정리되어 있으므로 필요할 때 들어가 보자

author도 django에서 지원해주는 유저계정인데 나중에 알아보도록 하자

아무튼 models.py에 이렇게만 작성하고 다음 명령어로 migrations 폴더를 만들어 줬다

    python manage.py makemigrations app
    
이 명령어는 app 폴더에 migrations 폴더를 만들고

models.py를 기반으로 새 마이그레이션을 생성한다

    python manage.py migrate 
    
라는 명령어로 models.py에서 만든 클래스를 django에서 여차저차 해서 데이터베이스로 만들어 준다

대충 말하자면 깃과 비슷하다

migration은 add와 commit으로, migrate는 push 로 생각하면 될것같다
