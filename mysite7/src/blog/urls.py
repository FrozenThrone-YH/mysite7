'''
Created on 2019. 8. 3.

@author: 405-3
'''
#blog/urls.py
from django.urls.conf import path
from blog.views import Main, Detail, Posting, post_delete

app_name = 'blog'
#view class는 등록 방법이 살짝 다르다.
#뷰클래스를 url에 등록할때는 뷰클래스.as_view()로 등록해야함
urlpatterns =[
    #main이라는 이름을 많이 쓰고 있지만, blog 그룹에 있는 main 이기에 구분이 가능하다. 
    #127.0.0.1:8000/blog/
    path("", Main.as_view(),name = 'main'),
    #DetailView는 특정모델클래스의 특정객체를 추출하기 위해 
    #pk라는 매개변수를 사용함 primary_key의 약자
    path("<int:pk>/", Detail.as_view(),name = 'detail'),
    path("posting/", Posting.as_view(), name = 'posting'),
    path("delete/<int:p_id>/",post_delete, name='delete')
    ]#as_view를 붙여줘야 뷰함수처럼 실행된다.
