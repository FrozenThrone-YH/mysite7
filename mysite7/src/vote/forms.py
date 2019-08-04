'''
Created on 2019. 7. 27.

@author: 405-3
HTML에 들어갈 <form>의 <input>을 관리하는 클래스 정의
'''
from django import forms
#Question 모델 클래스와 연동된 form 클래스 정의 
#모델 클래스와 Form클래스를 연동시킬려면 ModelForm클래스를 상속받아야함 
from vote.models import Question, Choice

class QuestionForm(forms.ModelForm):
    #ModelForm클래스에서 Meta클래스를 정의함으로써
    #어떤 모델클래스와 연동하는지 어떤 변수값을 사용할 것인지 표현
    class Meta:
        #model, fields, exclude
        #model :어떤 모델클래스와 연동했는지 저장하는 변수
        #fields와 exclude 중 한개의 변수를 사용해 사용할 변수 정의 
        model = Question
        fields = ['title'] #title변수값을 기입할 수 있도록 정의 
        #pub_date를 제외한 나머지 변수를 기입할 수 있도록 정의
        #exclude = ['pub_date'] 
        
#Choice 모델 클래스와 연동된 ChoiceForm 클래스 정의 
#q변수와 name변수를 접근할 수 있도록 설정 

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ['votes']
        # fields = ['q','name']
        
                