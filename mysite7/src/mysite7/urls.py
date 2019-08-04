"""mysite7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

urls.py : 웹 프로젝트가 실행될때 웹클라이언트가 요청을 한 인터넷주소에
해당하는 뷰 클래스/함수를 호출하기 위한 등록 파일 
뷰클래스/함수를 등록할때는 urlpatterns 변수의 요소로 추가하면 됨
요소로 추가할때는 path함수를 사용(import되있음)

path(웹클라이언트가 요청할 url주소(문자열), 호출될 뷰클래스/함수이름)

"""
from django.contrib import admin
from django.urls import path, include
#include : 다른 URLConf 파일을 등록할 때 사용하는 함수 
#path(시작문자열, include(urls.py가 있는 위치))
# -> 시작문자열로 요청하는 모든 인터넷 주소는 include안에 있는 
#Urls.py가 처리할 수 있도록 등록
#ex) path('test/', include('vote.urls'))
# -> 127.0.0.1:8000/test로 시작하는 모든 요청들을 vote폴더에 
#urls.py에서 처리할 수 있도록 등록 

#등록할 뷰함수를 import가 필요함 
from vote.views import test,test_value,test_input  #vote/views.py에 존재하는 test함수 import
from vote.views import main, detail, vote, result
from vote.views import q_registe, q_update, q_delete
from vote.views import c_registe, c_update, c_delete

urlpatterns = [
    path('a1/', admin.site.urls),
    path('',main),
    path('value/',test_value),
    #127.0.0.1:8000/숫자/로 요청하는 처리는 test_input 함수를 호출한다
    #호출할때 , 숫자값을 number변수에 인자값으로 사용한다. 
    path('<int:number>/',test_input),
    #path함수에 name 매개변수 : 등록된 뷰의 별칭을 등록하는 매개변수
    #템플릿 : {% url 별칭의 이름(문자열) %}
    #뷰 : reverse함수로 별칭 기반의 사이트 주소 추출가능
    path('vote/',main, name="main"),
    #127.0.0.1:8000/vote/숫자
    path('vote/<int:q_id>/',detail, name='detail'),
    path('vote/vote/',vote, name='vote'),
    path('vote/result/<int:c_id>/',result, name='result'),
    #127.0.0.1:8000/vote/qr/
    path('vote/qr/',q_registe, name='qr'),
    path('vote/qu/<int:q_id>/',q_update, name='qu'),
    #127.0.0.1:8000/vote/qd/q_id
    path('vote/qd/<int:q_id>/',q_delete, name='qd'),
        #127.0.0.1:8000/vote/cr/
    path('vote/cr/',c_registe, name='cr'),
    path('vote/cu/<int:c_id>/',c_update, name='cu'),
    #127.0.0.1:8000/vote/cd/c_id
    path('vote/cd/<int:c_id>/',c_delete, name='cd'),
    #127.0.0.1:8000/cl/로 시작하는 요청들은 
    #customlogin/url.py에서 처리 
    path('cl/',include('customlogin.urls')),
    
    #127.0.0.1:8000/auth/로 시작하는 요청들을
    #social_django 어플리케이션의 urls.py에서 처리
    #include함수의 namespace 매개변수 : 해당 urls.py에
    #지정된 app_name 값을 사용하지 않고 새로운 그룹명을 지정 (별칭으로 찾기 위해 별칭을 지정)
    #social_django.urls의미 - social_django 폴더 안에 있는 urls.py 파일 불러온다.
    path('auth/', include('social_django.urls',namespace='social')),
    
    #127.0.0.1:8000/blog/로 시작하는 요청들을 blog/urls.py에서 처리
    path('blog/', include('blog.urls'))
]
#settings.py 변수값을 사용할 수 있도록 import를 2개 해줘야 한다.
from django.conf import settings
# 1)MEDIA_URL과 MEDIA_ROOT를 연결하기 위한 함수 임포트
from django.conf.urls.static import static 
#/files/로 시작하는 모든 요청은 파일 업로드/다운로드 처리로 설정
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
