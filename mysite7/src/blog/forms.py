'''
Created on 2019. 8. 3.

@author: 405-3
'''
from django.forms.models import ModelForm
from blog.models import Post
from django.forms.fields import ImageField, FileField
from django import forms
from django.forms.widgets import ClearableFileInput

#ModelForm 자동완성(더블클릭)으로 import
class PostingForm(ModelForm):
    #사용자가 업로드할 파일/이미지를 입력받는 공간 생성 
    #import시 주의 사항 forms에 있는 ImageField import할것!
    #forms.ImageField : 사용자가 이미지를 선택할 수 잇는 입력공간
    #required : formsXXField의 공용 매개 변수로 사용자가 꼭 입력하지 않아도 되는 설정을 하는 매개변수  
    #여러개를 동시에 입력할 수 있게 하려면 위젯을 달아주면 된다.
    #ClearableFileInput : <input type ='file' 형태의 입력공간에   
    #                    파일관련 추가설정을 할 수 있는 위젯
    #multiple : True -> 하나의 입력공간에 여러개의 파일을 선택할 수 있도록 허용
    images = ImageField(required = False,
                        widget=ClearableFileInput(attrs={'multiple':True})) 
    #forms.ImageField()로 해도 된다. 
    #더블클릭해서 ClearableFileInput import
    
    #form class에 있는 FileField import 
    files = FileField(required = False,
                      widget=ClearableFileInput(attrs={'multiple':True}))
    
    class Meta :
        model = Post
        fields = ['category','title','content'] #사용자에게 입력 받을 것들 
