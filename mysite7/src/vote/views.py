from django.shortcuts import render, get_object_or_404

# Create your views here.
'''
views.py : MTV패턴 중 실직적인 데이터추출, 연산, HTML 전달의
기능이 구현되는 파일
view의 기능을 구현할 때는 클래스/함수를 정의해 사용할 수 있음.
함수를 정의해 view의 기능을 구현할때는 첫번째매개변수를 필수적으로 있어야 한다. 

request : 웹 클라이언트의 요청정보가 저장된 매개변수
request안에는 <form>를 바탕으로 사용자가 입력한 값이나 
로그인 정보, 요청방식 등을 변수형태로 저장하고 있다.
'''
#테스트용 뷰함수
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
def test(request):
    #render(request, HTML파일경로, 사전형데이터) 
    #해당요청을 보낸 웹클라이언트에게 전송할 HTML 파일을 
    #사전형데이터로 편집한 뒤 전송하는 함수
    #뷰함수는 반드시 HTML파일이나 다른사이트주소, 파일데이터를 
    #return 시켜야함. 
    return render(request,"test.html",{})

#뷰함수가 템플릿이 HTML을 변경할 수 있도록 변수값 전달 
    
def test_value(request):
    #render함수의 인자값으로 사용할 사전형 데이터 생성 
    dict = {'a':'홍길동님','b':[1,2,3,4,5]}
    #dict['a']
    return render(request,"test_value.html",dict)

def test_input(request,number):
    print(number)
    return render(request,"test_input.html",{'a':number})

#Question 모델 클래스 import 
from vote.models import Question,Choice
    
#메인화면 - 데이터 베이스에 저장된 Question객체를 바탕으로 HTML을 전달

def main(request):
    #데이터베이스에 저장된 모든 Question 객체를 추출
    '''
    Question.object : 데이터 베이스에 저장된 Question객체들을
    접근할때 사용하는 변수 
    객체를 접근할때는 4가지 함수로 접근할 수 있음.
    all():데이터 베이스에 저장된 모든 객체를 리스트형태로 추출
    get(조건):데이터 베이스에 저장된 객체 중 조건을 만족하는 객체 1개를 추출
    filter(조건) : 데이터베이스에 저장된 객체 중 조건을 만족하는 모든 객체를 리스트형태로 추출
    exclude(조건) : 데이터베이스에 저장된 객체 중 조건을 만족하지 않는 객체를 리스트형태로 추출 
    '''
    q = Question.objects.all()
    print(q)
    #추출된 Question 객체를 HTML 편집에 사용할 수 있도록 전달
    return render(request,"vote/main.html",{'q':q})

#웹 클라이언트가 요청한 Question객체 한개와 연결된 choice객체 추출 
#q_id : 웹클라이언트가 요청한 Question 객체의 id변수 값 
def detail(request,q_id):
    #Question 객체를 한개 추출 - id변수값이 q_id와 같은 조건에 맞는
    q = Question.objects.get(id=q_id)
    #추출한 Question객체와 연동된 Choice객체들을 추출
    #외래키로 연결된 Question객체가 Choice객체들을 대상으로 
    #추출함수를 사용하려면 객체.choice_set.추출함수로 추출
    #외래키로 연결된 객체.외래키로 연결한 모델클래스명_set.all,get 
    c = q.choice_set.all()
    print(q)
    print(c)
    #HTML코드로 추출한 객체들 전달 
    return render(request,"vote/detail.html",{'q':q,'c':c})

#detail 화면에서 웹클라이언트가 선택한 Choice객체 id로 투표 진행
@login_required
def vote(request):
    #조건문 - 사용자에게 요청한 방식이 post를 사용했는지 확인
    #request.method : 웹클라이언트의 요청방식을 저장한 변수 
    #"GET"또는 "POST" 문자열을 저장하고 있음 (모두 대문자이다.)
    if request.method == "POST": #request 변수로 연산자 수행
        #post요청으로 들어온 데이터 중 name=select에 저장된 값을 추출
        print(request.POST)
        c_id = request.POST.get('select') 
        #request에 다시 물어본다. POST는 사전형 데이터, select라는 이름으로 저장된 값을 얻고 싶다,   
        #POST요청으로 들어온 데이터는 request.POST에 사전형으로 저장됨
        #GET요청으로 들어온 데이터는 request.GET에 사전형으로 저장됨 
        #<form>태그에 작성된 사용자 입력을 추출할때는 name 속성에 적힌 문자열로 추출할 수 있다. 
        
        #Choice객체 한개 추출 - select 값을 id변수에 저장한 객체
        c = Choice.objects.get(id=c_id)
        
        #추출한 Choice객체 votes변수값을 +1누적
        c.votes = c.votes + 1
        
        #변경된 값을 데이터베이스에게 알려줌 
        c.save()
        
        #result 뷰 함수의 주소를 웹클라이언트에게 전송 
        #return HttpResponseRedirect('/vote/result/%s/'%(c.id))
        #별칭기반으로 result 뷰함수의 URL을 추출 및 전달
        return HttpResponseRedirect(reverse('result',args=(c.id,) ))
        '''
        HttpResponseRedirect(URL 문자열)
        : 웹 클라이언트에게 HTML이나 파일을 전달하는 것이 아닌 
        다른 뷰 함수의 URL주소를 넘겨주는 클래스. 웹클라이언트가
        리다이렉트 주소를 받으면 해당 주소로 웹서버에게 재 요청을 함.
        reverse(별칭문자열, args) : urls.py에서 등록한 별칭으로 URL주소를 반환하는 함수.
        '''
#Choice 객체의 id를 바탕으로 설문결과 출력
def result(request,c_id):
    #c_id 기반의 choice 객체 한개 찾기 
    c = Choice.objects.get(id=c_id)
    #Choice 객체와 연동된 Question 객체 추출


    # ~와 연동된 = ~. / ?의 객체 추출 = ~.!
    # q= Question.objects.get(id=c.q.id) #c에 연동된 q의 id값과 같은 Question 객체를 가져온다.
    q_2 = Question.objects.get(id=c.q.id)
    print(q_2)
    q = c.q
    print("c.q: ",c.q)
    print("q_2: ",q_2)
    print("q:",q)
    
    #Question객체와 연동된 모든 Choice객체 추출
    c_list = q.choice_set.all()
    #c_list=c.q.choice_set.all() 와 같음 
    
    #결과화면 HTML에 Quetion객체와 Choice 객체 리스트를 전달
    return render(request, "vote/result.html",{'q':q,'c_list':c_list})


'''
Question 객체 추가 함수
1)GET - 사용자에게 Question 객체를 생성할때 사용할 변수값을 입력
할수 있는 input 태그와 form 태그 제공
2)Post - 사용자가 입력한 데이터를 바탕으로 Qeustion 객체를 생성
및 데이터 베이스 저장
''' 
from vote.forms import QuestionForm
@login_required
def q_registe(request):
    #사용자 요청이 GET인지 POST인지 구분 
    if request.method == "GET":
        #GET으로 요청했을때는 HTML로 제공
        #QuestionForm 객체를 생성
        #QuestionForm 객체를 생성할 때 입력값이 없는 형태로 생성하면
        #Input 태그에 아무런 값도 입력되있지 않은 상태의 객체가 생성됨
        form = QuestionForm()   #QuestionFrom 객체 하나 생성
            
        #객체를 바탕으로 HTML 코드로 변환
       
        #as_p(),as_table,as_ul함수 : Form 객체에 입력할 수 있는
        #공간들을 <input>으로 변환하면서 <p>,<tr>,<td><li<태그로 
        #감싸누는 기능이 있는 함수
         
        rendered = form.as_p()
        print(rendered)
        #변환값을 HTML 파일에 전달 
        return render(request,"vote/q_registe.html",
                    {'rendered' : rendered})
    
    
    elif request.method == "POST":
        #POST로 요청했을때는 다른 주소를 제공
        #QuestionForm 객체를 생성 - 사용자 입력 바탕으로 생성
        form = QuestionForm(request.POST)
        #사용자가 입력한 값 기반으로 데이터 생성?
        
        #QuestionForm 객체와 연동된 Question 객체를 생성 및 저장
        #form.save(commit=False)
        # : 연동된 모델클래스의 객체로 변환만 하는 함수 
        # 데이터 베이스에 저장은 하지 않고 객체로 변경만?
        #form.save():연동된 모델클래스의 객체를 생성 및 데이터 베이스에 저장 
        new_q = form.save()
        print(new_q)
        #새로운 객체가 형성되었다.
        #생성된 Question객체의 id값으로 detail뷰의 링크를 전달
        return HttpResponseRedirect(
            reverse('detail',args=(new_q.id,)))
        
        
    
    

#Question 객체 수정 함수
#q_id : 사용자가 수정할 대상(Question)의 id값을 가지고 있다.
#에러시 사용자가 잘못요청했을때 다른 요청으로 해달라고 하는 에러 만들기 
#404 error - 4xx는 사용자 error(남탓하기) 
@login_required
def q_update(request,q_id):
    #수정할 Question 객체를 추출 하는 과정 필요
    #q_id: 어떤 객체를 수정할지 정보가 필요함
    #get_object_or_404 : 모델클래스의객체들중 id변수값을 이용해
    #객체 한개를 추출하는 함수. 단, 해당id값으로 된 객체가 없는 경우
    #사용자의 요청에 잘못있는 걸로 판단해 404에러 페이지를 전달한다.
    q = get_object_or_404(Question,id=q_id)
    #Question 객체들을 대상으로 id값이 q_id값이 동일한 녀석을 q에 저장하겠다.
    #단, id값이 없으면 404에러값을 사용자에게 전달하겠다.
    
    #조건문 - POST, GET인지 구분 필요
        #GET으로 요청시 QuestionForm 객체 생성 - 수정할 객체를 바탕으로 생성
        
    if request.method == "GET":
        #form 클래스 객체 생성시 instance매개변수에 연동된 객체를 전달하면 
        #해당 객체가 가진 값을 input태그에 채운 상태로 form 객체가 생성된다.
        form = QuestionForm(instance=q)
        #인스탄스 매개변수 사용하는 이유는 - 수정할때 수정하려는 것의 제목과 내용이 뜨도록 하기 위해서 (네이버 글 수정하듯이) 
        #as_table():각 입력공간과 설명을 <tr>과 <td>로 묶어주는 함수 
        result = form.as_table()
        return render(request,"vote/q_update.html",
                      {'result':result})
        #누구한테 보낼것이냐(request), 무엇을 보낼것이냐("html"), 그 값을 보낼때 어떤 값으로 수정해서 보낼것이냐(딕셔너리형태)
       
       #POST 요청시 QuestionForm 객체생성 - 수정대상객체 + 사용자 입력으로 생성
    elif request.method == "POST":
        #수정대상객체와 사용자입력으로 form객체 생성시
        #기존의 객체 정보를 수정한 상태의 form 객체가 생성됨
        form = QuestionForm(request.POST,instance=q)
        qq = form.save() #사용자입력으로 수정한 결과를 데이터베이스에 반영
        print(q, qq)
        #detail view로 이동
        return HttpResponseRedirect(reverse('detail',args=(q.id,)))
        


#Question 객체 삭제 함수
#GET - 정말로 지우시겠습니까?가 뜨는 HMTL 전달
#POST - 데이터베이스에 삭제처하는 처리 및 메인페이지 주소 전달
@login_required
def q_delete(request, q_id):
    q = get_object_or_404(Question,id=q_id)
    #q_id : 삭제할 대상
    if request.method == "GET":
        #form을 넘겨줄것이 아니라 rander함수를 써서 html을 리턴
        return render(request, "vote/q_delete.html",
                      {'q':q})
    elif request.method == "POST":
        #추출한 Question객체를 데이터베이스에서 제거 
        print("삭제할 대상의 id 변수값:",q.id)
        q.delete() #데이터베이스에 해당 객체 정보를 삭제하는 함수
        #삭제를 하더라도 id변수값을 제외한 변수들 값은 사용 할 수 있음. 
        print("삭제된 대상의 id변수값 :",q.id)
        print("삭제된 대상의 title:",q.title)
        return HttpResponseRedirect(reverse('main'))
    
from vote.forms import QuestionForm,ChoiceForm

#Choice 객체 추가
#GET - 빈 ChoiceForm 객체 생성 및 html 파일 전달\
#POST - 사용자 입력기반의 ChoiceForm 객체 생성및 
#데이터베이스에 객체 저장 - detail 뷰로 이동  
@login_required
def c_registe(request):
    #사용자 요청이 GET인지 POST인지 구분 
    if request.method == "GET":
        #GET으로 요청했을때는 HTML로 제공
        #ChoiceForm 객체를 생성
        #ChoiceForm 객체를 생성할 때 입력값이 없는 형태로 생성하면
        #Input 태그에 아무런 값도 입력되있지 않은 상태의 객체가 생성됨
        form = ChoiceForm()   #ChoiceFrom 객체 하나 생성
            
        #객체를 바탕으로 HTML 코드로 변환
       
        #as_p(),as_table,as_ul함수 : Form 객체에 입력할 수 있는
        #공간들을 <input>으로 변환하면서 <p>,<tr>,<td><li<태그로 
        #감싸누는 기능이 있는 함수
         
        c_rendered = form.as_p()
        print(c_rendered)
        #변환값을 HTML 파일에 전달 
        return render(request,"vote/c_registe.html",
                    {'c_rendered' : c_rendered})
    
    
    elif request.method == "POST":
        #POST로 요청했을때는 다른 주소를 제공
        #QuestionForm 객체를 생성 - 사용자 입력 바탕으로 생성
        form = ChoiceForm(request.POST)
        #사용자가 입력한 값 기반으로 데이터 생성?
        
        #QuestionForm 객체와 연동된 Question 객체를 생성 및 저장
        #form.save(commit=False)
        # : 연동된 모델클래스의 객체로 변환만 하는 함수 
        # 데이터 베이스에 저장은 하지 않고 객체로 변경만?
        #form.save():연동된 모델클래스의 객체를 생성 및 데이터 베이스에 저장 
        new_c = form.save()
        idx = new_c.q.id
        print(new_c)
        #새로운 객체가 형성되었다.
        #생성된 Question객체의 id값으로 detail뷰의 링크를 전달
        return HttpResponseRedirect(
            reverse('detail',args=(idx,)))
        #c.q.id = c객체에 연결된 Question의 id 
        
#Choice 객체 수정
#c_id : 수정할 choice객체의 id값
#공통 : 수정할 Choice 객체를 추출
#GET - 추출한 Choice객체 기반의 ChoiceForm객체 생성 및 html 전달
#POST - 추출한 Choice객체 + 사용자 입력 기반의 ChoiceForm객체 생성
# 및 수정 사항을 데이터베이스에 반영 - detail 뷰로 이동※c.id 이용
@login_required
def c_update(request, c_id):
    #수정할 Question 객체를 추출 하는 과정 필요
    #q_id: 어떤 객체를 수정할지 정보가 필요함
    #get_object_or_404 : 모델클래스의객체들중 id변수값을 이용해
    #객체 한개를 추출하는 함수. 단, 해당id값으로 된 객체가 없는 경우
    #사용자의 요청에 잘못있는 걸로 판단해 404에러 페이지를 전달한다.
    c = get_object_or_404(Choice,id=c_id)
    #Question 객체들을 대상으로 id값이 q_id값이 동일한 녀석을 q에 저장하겠다.
    #단, id값이 없으면 404에러값을 사용자에게 전달하겠다.
    
    #조건문 - POST, GET인지 구분 필요
        #GET으로 요청시 QuestionForm 객체 생성 - 수정할 객체를 바탕으로 생성
        
    if request.method == "GET":
        #form 클래스 객체 생성시 instance매개변수에 연동된 객체를 전달하면 
        #해당 객체가 가진 값을 input태그에 채운 상태로 form 객체가 생성된다.
        form = ChoiceForm(instance=c)
        #인스탄스 매개변수 사용하는 이유는 - 수정할때 수정하려는 것의 제목과 내용이 뜨도록 하기 위해서 (네이버 글 수정하듯이) 
        #as_table():각 입력공간과 설명을 <tr>과 <td>로 묶어주는 함수 
        c_result = form.as_table()
        detail_url = reverse('detail',args=(c.q.id,))
        return render(request,"vote/c_update.html",
                      {'c_result':c_result,'id':c.q.id,'detail_url':detail_url})
        #누구한테 보낼것이냐(request), 무엇을 보낼것이냐("html"), 그 값을 보낼때 어떤 값으로 수정해서 보낼것이냐(딕셔너리형태)
       
       #POST 요청시 QuestionForm 객체생성 - 수정대상객체 + 사용자 입력으로 생성
    elif request.method == "POST":
        #수정대상객체와 사용자입력으로 form객체 생성시
        #기존의 객체 정보를 수정한 상태의 form 객체가 생성됨
        form = ChoiceForm(request.POST,instance=c)
        cc = form.save() #사용자입력으로 수정한 결과를 데이터베이스에 반영
        idx = c.q.id
        print(c, cc)
        #detail view로 이동
        return HttpResponseRedirect(reverse('detail',args=(idx,)))
        


#Choice 객체 삭제 
#c_id : 수정할 choice객체의 id값
#공통 : 삭제할 Choice객체 추출 
#GET - 삭제 여부를 물어보는 HTML 파일 전달
#POST - 추출한 Choice 객체를 삭제 및 메인(또는 detail)로 이동
@login_required 
def c_delete(request, c_id):
    c = get_object_or_404(Choice,id=c_id)
    #q_id : 삭제할 대상
    if request.method == "GET":
        #form을 넘겨줄것이 아니라 rander함수를 써서 html을 리턴
        return render(request, "vote/c_delete.html",
                      {'c':c})
    elif request.method == "POST":
        #추출한 Question객체를 데이터베이스에서 제거 
        print("삭제할 대상의 id 변수값:",c.id)
        c.delete() #데이터베이스에 해당 객체 정보를 삭제하는 함수
        #삭제를 하더라도 id변수값을 제외한 변수들 값은 사용 할 수 있음. 
        print("삭제된 대상의 id변수값 :",c.id)
        print("삭제된 대상의 title:",c.name)
        return HttpResponseRedirect(reverse('detail',args=(c.q.id,)))