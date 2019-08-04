from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from blog.models import Post, PostFile, PostImage
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from blog.forms import PostingForm
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls.base import reverse

# Create your views here.


#글 목록이 뜨는 페이지
#ListView 자동완성 더블클릭하여 import 
#generic view - django에서 제공하는 여러가지 뷰 기능을 구현한 클래스 모음
#ListView : 특정 모델클래스의 객체들을 목록화할 수 있는 기능이 구현된 뷰  
class Main(ListView):
    #사용자에게 전달할 HTML파일의 경로
    #template_name은 지정된 변수 이름임 
    template_name = 'blog/main.html'
    
    #리스트로 뽑을 모델클래스 등록
    #Post 더블클릭해서 자동import 시키기
    model = Post
    
    #리스트로 추출한 객체를 HTML파일로 전달할때 사용할 이름
    context_object_name = 'list'
    
    #한페이지에 몇개의 객체가 보여질지 설정
    paginate_by = 5


#글 상세보기 페이지
#DetailView 더블클릭하여 자동 import
#DetailView : 특정 모델클래스의 특정 객체 한개를 추출할때 사용하는 뷰 
class Detail(DetailView):
    #사용자에게 전달할 HTML파일의 경로
    template_name = 'blog/detail.html'
    #리스트로 뽑을 모델클래스 등록
    model = Post
    #리스트로 추출한 객체를 HTML파일로 전달할때 사용할 이름
    context_object_name = 'obj'



#글 작성 페이지
#XXXMixin : 뷰클래스는 데코레이터를 지정할 수 없기 때문에 
#login_required와 같은 기능을 뷰에 지정하려면 XXXMixin클래스를 상속받으면 됨.
#단, 제네릭뷰를 먼저 상속받은 다음에 Mixin 클래스를 상속 받아야 정상적으로 기능이 동작한다. 
#LoginRequiredMixin : login_required 데코레이터와 동일한 기능 (@login_required)
#django.contrib.auth까지하면 라이브러리 이름까지

from django.contrib.auth.mixins import LoginRequiredMixin

#FormView :폼 클래스를 바탕으로 사용자에게 입력을 받는 처리 뷰
#Posting의 매개변수 순서 중요 
# - 순서가 바뀌면 비 로그인 상태에서도 글을 쓸 수 있음 
class Posting(LoginRequiredMixin, FormView):
    #사용자에게 전달할 HTML파일 경로
    template_name = 'blog/posting.html'

    #연동할 폼클래스의 이름
    #PostingForm 자동완성하여 자동 import
    form_class = PostingForm
    #GET방식으로 요청이 들어오면 등록된 폼클래스의 객체 생성 후 HTML 파일과 함께 전달
    #POST방식으로 요청이 들어오면 사용자의 입력을 바탕으로 폼클래스 객체 생성 후 
    #유효한 값인지(is_valid()) 확인한 뒤 Ture값이 반환되면 폼 객체를 저장하는 함수가 호출 
    
    
    #is_valid() 이후에 호출되는 함수를 오버라이딩해 사용자가 업로드한 
    # : 로그인을 했을때 아이디와 비밀번호가 형식에 맞는 지 확인하는 것 
    #이미지나 파일을 바탕으로 PostImage, PostFile 객체를 생성
    # form_valid는 유효할때 호출이 되는 것 자동완성해서 자동 import & 오버라이딩
    def form_valid(self, form):
        #form을 썼을때 save를 하면 바로 저장이 되었고, (매개변수commit=False면 저장이 안된다.) 
        #Form객체를 Post객체로 변환
        #Commit=False를 쓴 이유 : Post객체를 데이터베이스에 저장할 때 user변수에
        #값이 들어있지 않은 상태기 때문에 에러가 발생 
        #p에는 지금 post객체가 저장되어 있다. 
        #p : class에서 사용자 입력을 바탕으로 category, title, content변수가 채워져 있는
        #새로운 Post객체 => p.category / p.title / p.content를 쓸 수 있음
        # category, title, content는 앞으로 채워질거니까 빈칸으로 저장해져도 되는데
        # User라는 변수는 비어있으면 안된다. 그래서 저장을 하기 전에 user의 값을 써야한다.
        # Post class의 변수 5개 중 pub_date는 자동 / 카테고리,타이틀,콘텐츠는 앞으로 채울거니까 비어있도 되는데(blank=True설정), 유저는 비어있으면 안된다.  
        p = form.save(commit=False) #자동완성하면 안됨
        
        #user정보를 클라이언트의 유저정보로 대입 
        #user정보는 request.user라는 변수에 저장됨 (사용자 요청정보가 있는 정보) 
        #비로그인 상태는 None값이 저장되어 있다. 
        #self.request : 해당 뷰를 요청한 클라이언트의 요청정보가 저장된 변수 
        #slef.request.user : 요청한 클라이언트의 User모델클래스 객체저장 변수 
        p.user = self.request.user #최종 저장전 user를 채워준다. 
    
        
        #데이터베이스에 Post객체 저장 
        p.save() #새로운 객체 생성
        # 저장을 하려면 빈칸을 허용하거나, 빈칸이 없어야 한다.
        # 다른 데이터는 blank=True이기 때문이고, user는 blank가 true가 아니다. 
        # SET_NULL이라는 설정 값을 넣으면 user가 빈칸이어도 된다. 
        
        # 사용자가 입력한 것은 request.POST / request.GET 으로 저장된다. 
        # 사용자가 업로드한 파일 데이터를 바탕으로 PostFile 객체 생성
        # 사용자가 업로드한 파일의 갯수만큼 반복
        # self.request.FILES : 사용자가 업로드한 파일을 저장한 변수
        # self.request.FILES.getlist(name속성이름) 
        # : 해당 입력 공간에 업로드된 파일 데이터들을 추출
        for f in self.request.FILES.getlist('files'):
        #files라는 이름으로 날라온 파일들을 list로 만들어내서 하나씩 추출해서 f라는 이름으로 반복문에서 활용하겠다.
        #files라는 이름은 form class에서 name 속성이다.  
            #더블 클릭하여 자동 import/자동완성으로 안했을 경우 끝에 커서 대고 ctrl + space바 누르면 더블클릭하여 import 가능
            pf = PostFile() #post변수(외래키)와 file변수가 있음
                            #두 변수가 다 채워져야 저장이 된다.
            pf.post = p #새로만들어진 Post객체와 연동
            pf.file = f #사용자가 업로드한 파일을 FileField에 저장
            pf.save()   #두변수가 다 채워졌으므로 save
            
            
        
        # 사용자가 업로드한 이미지데이터를 바탕으로 PostImage객체 생성
        # 사용자가 'images' 입력공간에 업로드한 파일들을 바탕으로 객체생성을 하는 과정
        # forms.py에서 커스터마이징한 변수이름을 따오면 된다.  
        for i in self.request.FILES.getlist('images'):
            #새로운 PostImage 객체 생성 - 데이터베이스에 저장 x
            pi = PostImage()
            pi.post = p
            pi.image = i
            pi.save() 
            
        # blog:detail로 리다이렉트 
        # Detail view는 3개 변수 
        # 새로운 만들어진 Post객체의 id값으로 detail뷰의 주소 전달 
        return HttpResponseRedirect(
            reverse('blog:detail', args=(p.id,)))
        # 자동 import시 django.urls.base에서 제공하는 것으로 import
        #blog라는 그룹의 detail이라는 파일 
        
        #관리자 사이트에서 유저 정보의 활성값이 체크되는 것이 디폴트인데,
        #처음 아이디를 만들때 활성값이 비활성화되게끔하면 관리자 승인이 있어야지만 사용할 수 있게 된다.
        
#글 삭제 하기 
def post_delete(request, p_id):
    #post 객체 한개 추출 (2가지 방식)
    #자동 import 기능 활용 
    p = get_object_or_404(Post,id=p_id)
    
    #추출한 객체의 user정보와 요청한 클라이언트의 user정보를 비교
    #사용한 정보는 request에 있다. 
    if p.user == request.user :
        #자기가 쓴글을 지우는 요청인 경우, 추출한 객체를 삭제
        p.delete()
        #메인페이지로 이동
        return HttpResponseRedirect(reverse('blog:main'))
    else:    
        #자기가 쓴글이 아닌경우, 404Error 전달 
        #자동 import - 허용되지 않은 요청이다.
        return HttpResponseNotAllowed(["GET"])
        

