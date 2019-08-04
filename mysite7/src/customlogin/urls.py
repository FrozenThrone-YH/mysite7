'''
Created on 2019. 7. 28.

@author: 405-3
'''
from django.urls.conf import path
from customlogin.views import signup, signin, signout

#하위 urls.py를 정의 및 해당 어플리케이션 뷰함수를 등록
#app_name : 별칭기반으로 url을 찾을때 사용하는 그룹 이름
#ex) cl 그룹명에 signup 별칭을 가진 뷰함수를 찾을 경우
# url 'cl:signup' 콜론을 기준으로 왼쪽은 그룹명 오른쪽은 뷰함수
app_name = 'cl' #그룹 명 
#urlpatterns: path함수로 뷰함수를 등록 및 관리하는 변수
urlpatterns = [
    path('signup/',signup, name = 'signup'),
    path('signin/',signin, name = 'signin'),
    path('signout/',signout, name = 'signout')
    ] 

#app_name과 urlpatterns 이름은 고정이다. 없으면 에러가 뜬다. 