from django.shortcuts import render
from customlogin.forms import SigninForm,SignupForm
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.


'''회원가입'''

def signup(request):
#Get - 사용자에게 빈 회원가입란을 제공하는 HTML파일 전달
    if request.method == "GET":
        #SignupForm에서 입력할 수 있는 공간을 input태그로 변환
        result = SignupForm().as_table()
        return render(request,"cl/signup.html",{'result':result})
#POST - 사용자 입력을 바탕으로 회원가입 진행
    elif request.method == "POST":
        #사용자 입력을 바탕으로 객체 생성하고 
        form = SignupForm(request.POST)
        #사용자의 입력이 유효한 값이 있는지 확인(아이디 중목, e-mail 형식, 비밀번호 형식 확인)
        # -> is_valid() 함수 호출 결과가 True면 정상입력, False면 유효하지 않은 값 
        if form.is_valid():
            #is_valid함수의 결과가 True인 경우, form.cleaned_data변수로 원본 데이터를 접근할 수 있음
            #안그러면 회원가입란에 데이터베이스에 접근하는 문법을 치면 데이터가 수정이 되니까
            #비밀번호 란과 비밀번호 확인란이 같은 값이 있는지 확인
            if form.cleaned_data['password'] == form.cleaned_data['password_check'] :
                #User 객체 생성 및 데이터베이스에 저장
                #노가다가 좀 필요함 
                #User 모델 클래스는 비밀번호가 원본데이터가 아닌 암호화된 데이터를 저장한다.
                #새로운 User 객체를 생성할때 원본 비밀번호를 암호화해 객체생성해주는 함수를 사용해야한다.  
                # = > User.objects.create_user 함수를 사용하는 이유
                #create_user(id문자열, 이메일, 원본비밀번호 문자열)
                # = > 원본 비밀번호는 암호화된 상태로 새로운 User객체를 생성 및 반환
                new_user = User.objects.create_user(form.cleaned_data['username'],
                                         form.cleaned_data['email'],
                                         form.cleaned_data['password'])
                
                #성과 이름 저장변수에 사용자 입력을 대입 시킨다.
                new_user.first_name = form.cleane_data['first_name']
                new_user.last_name = form.cleane_data['last_name']
                
                #변경된 사항을 데이터베이스에게 통보
                new_user.save()
                
                #main 페이지로 이동 
                return HttpResponseRedirect(reverse('main'))
            

'''로그인'''
#GET - 폼 제공
#POST - 로그인 처리 
# 중요한 것은! 비밀번호는 암호화 된 상태에서 비교해야한다! 
def signin(request):
    if request.method == "GET" : 
        return render(request, "cl/signin.html",{'result':SigninForm().as_table()})
        #이번엔 한줄로 표현(이것이 최종 표현, 더이상 줄일 수 없다?) - 앞에서는 result에 할당하고 그것을 사용  
    elif request.method == "POST" :
        #is_valid는 회원가입시에 썼으니, 회원가입이 되어 있다면 is_valid는 False가 뜬다.
        #로그인 실패시 폼이 필요하다. (아이디나 비밀번호가 틀렸을때 전달할 form객체)
        form = SigninForm(request.POST)
        
        #아이디와 비밀번호 추출 
        id = request.POST.get('username') #request.POST는 딕셔너리 형태 이므로 
        pw = request.POST.get('password')
        #데이터베이스에 User객체들 중 아이디와 암호화된 비밀번호가 같은 객체 추출
        user = authenticate(username = id, password = pw) #자동완성- 더블클릭을 통해 import처리 필요
        print('데이터베이스에서 찾은 User 객체 :', user) #찾지 못하면 None을 갖는다. 
        #웹 클라이언트를 추출한 User 객체로 로그인 처리 
        #유저를 찾았으면 로그인 처리
        if user : #객체가 있다 True / None 값이면 False 
            #login(request, 추출한 user객체)
            #로그인처리가 된 웹클라이언트는 request.user를 사용할 수 있음
            # request.user.is_authenticated() : 해당 웹클라이언트가 로그인했으면 True, 안했으면 False
            # 함수 앞이 is_로 시작하면 True or False값으로 반환
            login(request,user)#1번째 클라이언트에 대한 요청 2번째 어떤 유저정보로 로그인을 시킬거니?
            return HttpResponseRedirect(reverse('main'))
        
        #못 찾았으면 잘못입력했다고 알려주기 
    

#로그아웃
def signout(request):
    #logout(request) : 해당 요청을 한 웹 클라이언트의 user정보를 제거
    #request.user에 None값이 저장됨 
    logout(request)
    
    #cl그룹의 signin 별 칭을 가진 뷰의 인터넷주소를 클라이언트에게 전달
    return HttpResponseRedirect(reverse("cl:signin"))