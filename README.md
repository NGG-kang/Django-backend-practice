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


### 3. templates

여기부턴 일단 내 생각대로 적고 정리하는 시간 / 지금 이해하는 중이라 따로 정리 할 수가 없다

url, views, templates 이 셋이 화면 구성에는 가장 중요한 역할이다

models도 데이터관련으로 중요하긴 하다만 정작 본인이 제대로 보질 않아서 일단 화면구성에 중점을 두었다

#### urls 생각 정리

urls.py 의 app_name 정리

html에서 href의 urls을 정할 때 {% url app:name %}를 쓰잖아?

그게 알고보니까 urls.py의 app_name에서 적은게 {% url %}로 가는거더라

app은 설치한 app name이고 ':' 뒤의 name은 urls.py에 적은 path의 name들

아 어떻게 이어지나 했더니 app_name과 설치한 app이름과, path의 name으로 이어지는거였네... 정말 대단해~~

app_name은 끝

url.py는 기본 startproject를 제외한 startapp 에서는 없으므로 따로 만들어 줘야 한다

먼저 자동으로 만들어진 project의 urls.py이다

```python
urlpatterns = [
    path('', include('pcsub.urls')),
    path('pcsub/', include('pcsub.urls')),
    path('common/', include('common.urls')),
    path('admin/', admin.site.urls),
]
```
django에서 지원하는 include, path를 활용해서 각 폴더의 urls.py에 접근 할 수가 있다

그래서 이번 프로젝트에 만든 pcsub, common을 추가 해 줬다

admin은 django에서 자동으로 만들어 준 것이다

다음으로 app으로 따로 생성한 app의 urls.py이다

```python
app_name = 'pcsub'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('write/', views.write.as_view(), name='write'),
    path('<int:pk>/', views.Detail.as_view(), name='detail'),
    path('<int:pk>/delete', views.deleteBoard, name='delete'),
    path('<int:pk>/modify', views.Modify.as_view(), name='modify'),
    path('<int:pk>/modify/modifyBoard/', views.modifyBoard, name='modifyBoard'),
    path('write/writeBoard/', views.writeBoard, name='writeBoard'),
]
```
어우 생각보다 많다

먼저 path의 첫번쨰는 주소창에 나타날 이름이다

두번째는 views.py와 연결되어 거기에 쓰인 Class나 def들을 불러오는 것이고

세번째는 html상에서 쓰이게 될 url name이다 

#### views 생각 정리
