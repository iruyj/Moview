import random
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.template import RequestContext
from .models import Moviews
from .forms import MoviewForm

# render : 파이썬 데이터를 템플릿 에 적용하여 HTML로 반환하는 함수
# Create your views here.
def index(request):
    # 영화목록 출력
    kw = request.GET.get('kw','')

    # order_by : viewdate순으로 -붙여서 역방향
    mlist = Moviews.objects.order_by('-viewdate')
    if kw:
        mlist = mlist.filter(
            Q(moviename__icontains=kw)  | # 영화이름 검색
            Q(author__username__icontains=kw) | # 작성자 검색
            Q(moviewline__icontains=kw)
        ).distinct()    # 중복제거
    # moview 데이터를 moview.index.html에 적용하여 HTML 리턴함
    # 랜덤으로 배경 스타일 주기
    style = ['style1','style2','style3','style4','style5','style6']
    randoms = list()
    for i in range(len(mlist)):
        randoms.append(random.choice(style))
    context = {'multilist' : zip(mlist,style), 'kw':kw, 'user':request.user}
    return render(request, 'moview/index.html', context)

def add_movie(request):
    # 뮤비 추가
    if request.method == 'POST':
        form = MoviewForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = request.user
            movie.moviewimg = request.FILES.get('moviewimg')
            movie.save()
            return redirect('moview:index')
    else:
        form = MoviewForm()
    context = {'form':form}
    return render(request, 'moview/create.html',context)


def movie_detail(request, movie_id):
    # 해당 영화일기의 내용 출력 : pk - 해당 아이디인것만 가져오기
    movies = get_object_or_404(Moviews, pk=movie_id)
    is_user = request.user== movies.author     # 지금 로그인된 유저가 작성한 게시물인지
    context = {'moview': movies, 'is_user':is_user}
    return render(request, 'moview/generic.html', context)

# 해당 함수 역시 로그인이 필요하기때문에 어노테이션 넣음
@login_required(login_url='common:login')
def movie_delete(request: object, movie_id):
    # 질문삭제 : 사용자, 글쓴이가 동일한 경우에만
    movie = get_object_or_404(Moviews, pk=movie_id)
    if request.user != movie.author:
        messages.error(request, "삭제권한이 없습니다.")
    else:
        movie.delete()
    return redirect('moview:index')


def movie_update(request, movie_id):
    movie = get_object_or_404(Moviews, pk=movie_id)
    if request.user != movie.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('moview:detail', movie_id)

    if request.method == "POST":
        form = MoviewForm(request.POST,request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.moviewimg = request.FILES.get('moviewimg')
            movie.save()
            return redirect('moview:index')
    else:
        form = MoviewForm(instance=movie)
    context = {'form': form,'movie':movie}
    return render(request, 'moview/modify.html', context)

def movie_choose(request):
    movie = random.choice(Moviews.objects.all())    #랜덤으로 한개 정하기
    return redirect('moview:detail', movie.id)


def movie_my(request,username):
    movies = Moviews.objects.order_by('-viewdate').filter(
        Q(author__username__contains=username)
    ).distinct()
    style = ['style1', 'style2', 'style3', 'style4', 'style5', 'style6']
    randoms = list()
    for i in range(len(movies)):
        randoms.append(random.choice(style))
    context = {'multilist': zip(movies, style), 'kw': ''}
    return render(request, 'moview/mypage.html',context)


def start(request):
    is_user = request.user  # 지금 로그인된 유저가 작성한 게시물인지
    context = {'user': is_user}
    return render(request, 'moview/start.html')


def limit_user(request):
    return render(request, 'limit.html')