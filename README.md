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



## 코드 및 이해 한 내용 정리

다음으로는 

게시판을 만들면서 사용한 코드와 내용을 내가 이해 한 대로 정리한 것이다



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



### 3. urls, views의 관계


여기부턴 일단 내 생각대로 적고 정리하는 시간 / 지금 이해하는 중이라 따로 정리 할 수가 없다

url, views, templates 이 셋이 화면 구성에는 가장 중요한 역할이다

models도 데이터관련으로 중요하긴 하다만 정작 본인이 제대로 보질 않아서 일단 화면구성에 중점을 두었다


#### urls 생각 정리

url.py는 기본 startproject를 제외한 startapp 에서는 없으므로 따로 만들어 줘야 한다

먼저 자동으로 만들어지고, app을 추가한 project의 urls.py이다

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
어우 많다

먼저 path의 첫번쨰는 주소창에 나타날 이름이다

<int:pk>는 board에서 쓸 id값을 넘겨주는건데 여기서 pk라는 이름도 views.py와 연결되어 사용하는 이름이므로 신중히 정하자

두번째는 views.py와 연결되어 거기에 쓰인 Class나 def들을 불러오는 것이고

세번째는 html상에서 쓰이게 될 url name이다 



#### views 생각 정리

urls.py와 연결되어있는 views.py이다

class나 def로 models와 연결하여 urls로 뿌려주는 역할이다

프로젝트의 index class를 먼저 보자
```python
class IndexView(generic.ListView):
    template_name = 'pcsub/index.html'
    context_object_name = 'board_list'

    def get_queryset(self):
        return Board.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
```
board의 index에 맞춰서 ListView를 사용하여 board를 list로 가져왔다
 
template_name은 index 페이지의 위치를 지정하는 것인데 django에서 지원해 주는 속성이다

만약 template_name이 없으면 django에서 자동으로 인식해서 맞춰준다

이 template_name을 지정하기 전에 Templates 폴더를 지정 해줘야 하는데

project/settings.py에 TEMPLATES의 DIRS 부분에 project에서 templates를 저장 할 DIR를 정하면 된다


다음으로 context_object_name

이것도 django에서 기본적으로 제공하는 속성이다

ListView를 반환하는데 이름을 따로 지정해주는데 사용하는게 context_object_name이다

```
class Detail(generic.DetailView):
    template_name = 'pcsub/detail.html'
    model = Board
```
Detail 이라는 views의 클래스인데 여기서는 안쓰고 model = Board 처럼 데이터만 넘겨줬다


다음으로 get_queryset [Django](https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/#generic-views-of-objects) 참조

ListView에는 get_queryset()재정의 할 수 있는 메서드가 있다. 

기본적으로 queryset속성 값을 반환 하지만 더 많은 로직을 추가하는 데 사용할 수 있다

여기서는 시간을 저장한 pub_date를 정렬하여 5개까지 보내주는데에 쓰였다


그 외에도 글 작성과 수정 삭제의 request가 있는데 그것은 templates의 html부분과 views.py, urls.py와 연결지어 다시 설명하겠다



### 4. urls, views, templates의 관계

urls.py, views.py, templates의 html의 연관 관계를 설명한다.


#### urls.py와 views.py

urls.py 의 app_name 

html에서 다음 페이지로 넘어갈 때 href의 urls을 정할 때 {% url app:name %}를 쓴다

그게 알고보니까 urls.py의 app_name에서 적은게 {% url %}로 가는것

app은 설치한 app name이고 ':' 뒤의 name은 urls.py에 적은 path의 name들

아 어떻게 이어지나 했더니 app_name과 설치한 app이름과, path의 name으로 이어지는 것 이었다

예시로 urls.py에

    path('', views.IndexView.as_view(), name='index'),
    
이러한 코드가 있다고 치자

{% url app:name %} 

위의 url은 urls.py의 app_name이 자동 적용

app은 app_name과 동일하다고 생각하면 된다 

name은 위의 path의 name명이 그대로 사용된다


#### urls.py 와 templates

기본적으로 path의 첫번째로 쓰는 주소가 html의 주소로 적용된다

    path('<int:pk>/', views.Detail.as_view(), name='detail'),
    
만약 저런 urls의 path가 있다면 주소는 
ex) 127.0.0.1:8080/pk/write 로 적용된다. 여기서 pk는 값이다

다음으로 path의 <int:pk>는 url로 날라가는데 아래를 보자

{% url 'pcsub:detail' board.id %}

html의 href 코드에 이렇게 적어주는데 뒤의 board.id로 <int:pk>값을 넘겨 주는 것이다

pcsub:detail의 주소는 ('<int:pk/') 이므로 


#### views.py와 templates

위에서는 Board DB에서 값을 불러오느라 views와 templates의 접점이 딱히 없었다

하지만 write modify delete로 들어가면 접점이 생긴다

아래의 코드는 views.py의 modifyBoard 함수이다

```python
def modifyBoard(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pcsub:modify', pk=board.id)
    if request.method == 'POST':
        title = request.POST.get('title', 'None')
        context = request.POST.get('context', 'None')
        pub_date = timezone.now()
        board.title = title
        board.context = context
        board.pub_date = pub_date
        board.author = request.user
        board.save()
    return redirect('pcsub:detail', pk=board.id)
```
modify에서는 수정작업 이므로 request와 pk라는 인자를 받는다

다음은 get_object_or_404(Board, pk=pk)라는게 나온다

이것의 의미는 url에서 board.id를 보내주는게 있지 않았나?

그것의 이름이 pk로 넘어와 이 pk에 맞는 Board의 값을 받아온다(없으면 404 호출)

다음으로 request는 html에서 form의 POST로 전달받은 값들이다

request.POST.get('name',default)로 값을 받을 수 있다 (defalut는 생략 가능)

현재 변수 board는 pk에 맞는 Board 값 이므로 값을 교체 하고, board.save()하여 값을 세이브 한다

return redirect로 수정 후의 게시판을 보여준다



### 5. Templates

teamplates에서도 django에 지원하는 코드들이 많이 있다

괄호와 %를 쓰면 django가 지원하는 메소드를 사용 할 수 있다 {% methon %}

{% for a in a_list %} {% endfor %}

{% if a %} {% else %} {% endif %}

{% load static %}

for문이나 if문을 사용 하려면 end문을 꼭 써줘야 한다

괄호가 2개씩 들어가면 불러온 값들을 출력 할 수 있다  {{ 값 }}



### 6. User author

추가 예정

### 7. 기타

admin 페이지 지원, models 의 데이터를 어드민 페이지에 추가 하는거 / 추가 예정
