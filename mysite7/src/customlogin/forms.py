'''
Created on 2019. 7. 28.

@author: 405-3
'''
#Django에서 기본적으로 제공해주는 회원관리 어플리케이션에서 
#User 모델클래스를 연동해 회원가입, 로그인 폼을 정의 
#django.contrib.auth 이걸 불러 올 것이다.
#python - lib(라이브러리) - site- packages(웹에서 다운 받은 라이브)
# - django - contrib - auth -> 여러 py와 폴더들이 있다.
# 그중에 models.py에 있는 class에 접근할 것.

#django.contrib.auth.models : 장고에서 회원관리를 하는 어플리케이션 경로

from django.contrib.auth.models import User
# User.is_authenticated: 지금 접속해 있는지 아닌지 판단

'''회원가입 폼'''
from django import forms 
class SignupForm(forms.ModelForm):
    #ModelForm를 상속 받으면 Meta 클래스를 재정의 해줘야한다.
    #지정된 변수들을 사용해야한다. 
    
    '''모델클래스의 변수 외에 비밀번호 확인란을 추가'''
    #forms.XXXXField : 폼클래스에 사용자 입력공간을 정의할때 사용
    #모델클래스에서 사용한 models.XXXField와 기능과 이름이 유사함
    #label 매개변수 : 해당 입력공간의 설명란을 정의하는 매개변수 
    #기본 값은 변수명으로 설정됨 
    
    #위젯 : 데이터저장형식 외에 사용자의 입력타입을 변환하는 것 
    #비밀번호 작성란은 텍스트 값을 입력받기 때문에 type = text로 되어 있지만
    #비밀번호 타입으로 바꿔주는 작업은 위젯을 통해 할 수 있음 
    password_check = forms.CharField(max_length = 100, label='비밀번호 확인',widget = forms.PasswordInput())
    #widget = forms.PasswordInput() 이걸 하면 비밀번호확인란에 입력하면 다른 표시가 되어 표기 된다. 
    
    
    #입력란의 순서를 저장하는 변수
    field_order = ['username','password','password_check',
                   'last_name','first_name','email']
    
    class Meta:
        model = User
        #User에 무슨 변수가 있는지 확인 (ctrl key + User 클릭)
        fields = ['username','password','last_name','first_name',
                  'email']
        #모델 클래스에 정의된 변수를 대상으로 위젯을 적용할때 사용하는 변수 
        widgets = {
            #'변수이름':적용할 위젯 (xxxInput클래스 객체)
            'password' : forms.PasswordInput()            
            }
        #비밀번호 확인란은 class에 없고, 단순히 password가 같은지만 보면 되니까
        
'''로그인에 사용할 폼클래스 정의'''
class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password'] 
        widgets = {
            'password' : forms.PasswordInput()
            }