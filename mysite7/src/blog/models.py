from django.db import models

# Create your models here.
#django에서 제공하는 회원모델 클래스
#1명의 User가 여러개의 글을 작성할수 있도록 외래키 설정
from django.contrib.auth.models import User

#글 카테고리 
class Category(models.Model):
    #카테고리명
    #CharField의 첫번째 매개변수는 별칭
    #CharField의 두번째 매개변수는 글자수(자동완성하면 안됨)
    name = models.CharField('카테고리',max_length=10)
    #객체 출력 함수 오버라이딩
    #__str치면 자동완성에 오버라이딩이라고 뜬다.(더블클릭으로 자동완성)
    def __str__(self):
        return self.name
    

#글 내용을 저장
class Post(models.Model):
    #Category 모델클래스 외래키 설정
    #Post가 N이 되고 Category가 1이된다. 
    #ForeignKey(연결할 클래스, 외래키가 삭제된 경우)
    #models.PROTECT : Category객체가 삭제가 될 때, 연결된 Post 객체가 존재하면
    #삭제 되지 않도록 막아주는 기능 
    #ex) 네이버카페는 등록된 모든 글을 지워야 삭제 가능 : PROTECT가 되어 있어서 그렇다. 
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    #User 모델클래스 외래키 설정
    #누가 그 글을 남겼는지 정보 설정
    #models.CASCADE : User객체가 삭제될때, 연결된 Post객체들도 같이 삭제되는 기능 
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    
    #제목
    title = models.CharField('제목',max_length=100)
    
    #글 내용
    #TextField : 글자수 제한이 없는 문자열 저장 공간
    #blank,null : xxxField 생성자의 공통 매개 변수 
    #blank : form태그에서 필수로 입력하지 않아도 되는 영역 설정
    #null : 데이터 베이스에 저장할때 값이 없어도 저장되도록 설정
    content = models.TextField('내용',blank=True, null = True)
    
    #생성일 
    #auto_now_add = True : 객체생성시 서버의 시간을 자동으로 입력하는 설정
    pub_date = models.DateField('작성일',auto_now_add=True)
    def __str__(self):
        return self.title #명확하게 확인 가능 
    
    #Meta 클래스 정의해 정렬순서를 지정
    class Meta:
        #지정된 값을 넣으면 정렬되는?
        #정렬 순서 지정
        #정렬에 사용할 변수들을 리스트형태로 지정 
        #pub_date - 날짜순으로 하겠다. 기본은 오름차순이다.(옛날 것이 먼저 나온다.)
        #-pub_date : 앞에 '-'를 붙이면 내림차순으로   
        ordering = ['-pub_date']
    

#글에 포함된 이미지
class PostImage(models.Model):
    #어떤 글의 객체인지 연결(외래키로)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    #이미지파일 저장공간 생성
    #ImageField : 이미지를 저장할때 사용하는 저장공간
    #'이미지'는 별칭
    #upload_to : 클라이언트가 업로드한 파일을 저장 및 접근할때
    #사용할 이미지가 저장된 서버의 하드디스크 경로
    #%Y : 서버 시간 기준의 년
    #%m : 서버 시간 기준의 월, %d : 서버 시간 기준의 일
    #클라이언트가 이미지를 업로드하면 images/년/월/일 폴더에 저장함
    image = models.ImageField('이미지',upload_to='images/%Y/%m/%d')
    

#글에 포함된 파일
class PostFile(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    #클라이언트가 업로드한 파일들은 서버의 files/년/월/일 폴더에 저장됨
    file = models.FileField('파일',upload_to='files/%Y/%m/%d')

