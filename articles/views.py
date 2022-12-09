from django.shortcuts import render, redirect
from .models import *
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from main.models import Song
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth import get_user_model

# 위치 api 구현
from .gmap import reverse_geocoding, parsing_geocoded
import os
import pprint
import json

# Create your views here.
def private(request):
    comment_form = CommentForm()

    # 임시로 서울로 설정함. 현재 위치 받아오게 되면 현재 위치 기준으로 설정하면 됨.
    song_queryset = (
        Article.objects.filter(place__icontains="서울")
        .values("song")
        .annotate(Count("id"))
    )
    song_list = []
    for song_id in song_queryset:
        song = Song.objects.get(id=song_id["song"])
        song_list.append(song)

    # 해당 위치 작성 글 가져오기
    articles = Article.objects.filter(place__icontains="서울").order_by("-pk")
    if articles:
        top_article = Article.objects.filter(place__icontains="서울").order_by("-pk")[0]
    else:
        top_article = ""

    context = {
        "comment_form": comment_form,
        "top_article": top_article,
        "articles": articles,
        "song_list": song_list,
    }
    return render(request, "articles/private.html", context)


def index(request):
    # 임시로 서울로 설정함. 현재 위치 받아오게 되면 현재 위치 기준으로 설정하면 됨.
    song_queryset = (
        Article.objects.filter(place__icontains="서울")
        .values("song")
        .annotate(Count("id"))
        .order_by('-id__count')
    )
    song_list = []
    for song_id in song_queryset:
        song = Song.objects.get(id=song_id["song"])
        song_list.append(song)
    carousel_list = song_list[1:]
    articles = Article.objects.filter(place__icontains="서울").order_by("-pk")
    context = {
        "articles": articles,
        "song_list": song_list,
        "carousel_list": carousel_list,
    }
    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        place = request.POST.get("place", "")
        content = request.POST.get("content", "")
        vidid = request.POST.get("vidid", "")
        vidtitle = request.POST.get("vidtitle", "")
        channel = request.POST.get("channel", "")
        hqdefault = request.POST.get("hqdefault", "")
        default = request.POST.get("default", "")
        mqdefault = request.POST.get("mqdefault", "")
        print(vidid, place, content)
        if vidid and place and content:
            try:
                song = Song.objects.get(vidid=vidid)
            except:
                song = Song.objects.create(
                    vidid=vidid,
                    title=vidtitle,
                    channel=channel,
                    hqdefault=hqdefault,
                    default=default,
                    mqdefault=mqdefault,
                )
            Article.objects.create(
                user=request.user,
                place=place,
                content=content,
                song=song,
            )
            return redirect("articles:index")
        else:
            return redirect("articles:create")
    context = {
    }
    return render(request, "articles/create.html", context)


@login_required
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    like = Like.objects.all()
    comment_form = CommentForm()
    context = {
        "article": article,
        "like": like,
        "comments": article.comment_set.all(),
        "comment_form": comment_form,
    }
    return render(request, "articles/detail.html", context)


@login_required
def delete(request, pk):
    Article.objects.get(pk=pk).delete()
    return redirect("articles:index")


@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        place = request.POST.get("place", "")
        content = request.POST.get("content", "")
        vidid = request.POST.get("vidid", "")
        vidtitle = request.POST.get("vidtitle", "")
        channel = request.POST.get("channel", "")
        hqdefault = request.POST.get("hqdefault", "")
        default = request.POST.get("default", "")
        mqdefault = request.POST.get("mqdefault", "")
        print(vidid, place, content)
        if vidid and place and content:
            try:
                song = Song.objects.get(vidid=vidid)
            except:
                song = Song.objects.create(
                    vidid=vidid,
                    title=vidtitle,
                    channel=channel,
                    hqdefault=hqdefault,
                    default=default,
                    mqdefault=mqdefault,
                )
            article.user = request.user
            article.place = place
            article.content = content
            article.song = song
            article.save(update_fields=["user", "place", "content", "song"])
            return redirect("articles:index")
        else:
            return redirect("articles:update", pk)
    context = {
        "article": article,
    }
    return render(request, "articles/update.html", context)


def location_get(request):
    print(request.POST.get("userLocation"))
    print(request.POST.get("markerLocation"))
    # 위치 정보 가져오기 : google geolocation api 요청
    gmap_api_key = os.getenv("gmap_api")
    user_location = request.POST.get("userLocation")
    marker_location = request.POST.get("markerLocation")
    if request.method == "POST" and user_location:
        user_coords = user_location.split(",")
        user_loc = parsing_geocoded(user_coords[0], user_coords[1])["loc"]
        user_place = Place.objects.create(name=user_loc[0])
    else:
        user_loc = ["somewhere"]
        user_position = ["somewhere"]
    # Place 테이블에 geocoding된 위치 값을 저장한다. => 위치 지속적으로 업데이트 되도록 해야함
    user_position = Place.objects.order_by("-id").values()[0]["name"]
    context = {
        "user_position": user_position,
        "key": gmap_api_key,
    }
    return render(request, "articles/locations.html", context)


def clicked_location(request):
    return redirect("articles:location_test")


def location_test(request):
    clicked_location = request.POST.get("clicked")
    user_position = " ".join(
        Place.objects.order_by("-id").values()[0]["name"].split(" ")[3:5]
    )
    context = {
        "user_position": user_position,
        "clicked": clicked_location,
    }
    # 주소명 장소명으로 변환하기
    # DB 방식 변경하기
    # 마커, 현재위치버튼
    return render(request, "articles/locationInputTest.html", context)


def public(request):
    # place model에서 필드를 가져온다.
    users = get_user_model().objects.all()
    places = Article.objects.filter(place="서울")
    context = {
        "places": places,
        "users": users,
    }
    return render(request, "articles/public.html", context)


def test(request):
    return render(request, "articles/test.html")


@login_required
def like(request, pk):

    article = Article.objects.get(pk=pk)

    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True

    like_count = article.like_users.count()

    context = {
        "is_liked": is_liked,
        "likeCount": like_count,
    }
    return JsonResponse(context)


def comment_create(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
    context = {
        "content": comment.content,
        "username": comment.user.username,
    }
    return JsonResponse(context)


def song(request):
    context = {}
    return render(request, "articles/song.html", context)


def song_detail(request, video_id):
    song = Song.objects.get(vidid=video_id)
    articles = Article.objects.filter(song=song)
    context = {
        "song": song,
        "articles": articles,
    }
    return render(request, "articles/song_detail.html", context)
