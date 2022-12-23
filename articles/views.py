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

# redis
# from django.core.cache import cache

# Create your views here.
def private(request):
    if request.method == "POST":
        place = request.POST.get("place-to-view-input", "")
        comment_form = CommentForm()

        song_queryset = (
            Article.objects.filter(place__icontains=place)
            .values("song")
            .annotate(Count("id"))
        )

        if song_queryset:
            top_song = Song.objects.get(id=song_queryset[0]["song"])
        else:
            top_song = ""

        song_list = []
        for song_id in song_queryset[1:]:
            song = Song.objects.get(id=song_id["song"])
            song_list.append(song)

        # 해당 위치 작성 글 가져오기
        articles = Article.objects.filter(place__icontains=place).order_by("-pk")
        if articles:
            top_article = Article.objects.filter(place__icontains=place).order_by(
                "-pk"
            )[0]
        else:
            top_article = ""

        context = {
            "comment_form": comment_form,
            "top_article": top_article,
            "articles": articles,
            "top_song": top_song,
            "song_list": song_list,
            "place": place,
        }
        return render(request, "articles/private.html", context)
    place = request.COOKIES.get("key") or "서울"
    print(place)
    comment_form = CommentForm()
    song_queryset = (
        Article.objects.filter(place__icontains=place)
        .values("song")
        .annotate(Count("id"))
    )

    if song_queryset:
        top_song = Song.objects.get(id=song_queryset[0]["song"])
    else:
        top_song = ""

    song_list = []
    for song_id in song_queryset[1:]:
        song = Song.objects.get(id=song_id["song"])
        song_list.append(song)

    # 해당 위치 작성 글 가져오기
    articles = Article.objects.filter(place__icontains=place).order_by("-pk")
    if articles:
        top_article = Article.objects.filter(place__icontains=place).order_by("-pk")[0]
    else:
        top_article = ""

    context = {
        "comment_form": comment_form,
        "top_article": top_article,
        "articles": articles,
        "top_song": top_song,
        "song_list": song_list,
        "place": place,
    }
    return render(request, "articles/private.html", context)


def index(request):
    if request.method == "POST":
        kw = request.POST.get("kw", "")
        song_queryset = (
            Article.objects.filter(place__icontains=kw)
            .values("song")
            .annotate(Count("id"))
            .order_by("-id__count")
        )
        song_list = []
        for song_id in song_queryset:
            song = Song.objects.get(id=song_id["song"])
            song_list.append(song)
        print(song_list)

        articles = Article.objects.filter(place__icontains=kw).order_by("-pk")
        article_list = []
        for article in articles:
            article_dict = {}
            article_dict["pk"] = article.pk
            article_dict["user"] = article.user.username
            try:
                article_dict["user_img"] = article.user.user_img.url
            except:
                article_dict[
                    "user_img"
                ] = "https://e7.pngegg.com/pngimages/1000/665/png-clipart-computer-icons-profile-s-free-angle-sphere.png"
            article_dict["content"] = article.content
            article_dict["song_vidid"] = article.song.vidid
            article_dict["song_title"] = article.song.title
            article_dict["song_channel"] = article.song.channel
            article_dict["img"] = article.song.hqdefault
            article_list.append(article_dict)
        data = {
            "article_list": article_list,
            # "song_list": song_list,
        }
        return JsonResponse(data)
    return render(request, "articles/index.html")


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
            new_article = Article.objects.create(
                user=request.user,
                place=place,
                content=content,
                song=song,
            )
            return redirect("articles:detail", new_article.pk)
        else:
            return render(request, "articles/create.html")
    return render(request, "articles/create.html")


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
    return redirect("articles:private")


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
            return redirect("articles:detail", article.pk)
        else:
            return redirect("articles:update", pk)
    context = {
        "article": article,
    }
    return render(request, "articles/update.html", context)


def location_get(request):
    # 위치 정보 가져오기 : google geolocation api 요청
    user_location = request.POST.get("userLocation")
    if request.method == "POST":
        user_coords = user_location.split(",")
        user_loc = parsing_geocoded(user_coords[0], user_coords[1])["loc"]
        # user_place = Place.objects.create(name=" ".join(user_loc[0].split(" ")[3:5]))
    else:
        user_position = "somewhere"
    user_position = Place.objects.order_by("-id").values()[0]["name"]
    # user_coords_save = Place.objects.create(coords=user_coords)
    # user_current_coords = Place.objects.order_by("-id").values()[0]["coords"]
    # Place 테이블에 geocoding된 위치 값을 저장한다. => 위치 지속적으로 업데이트 되도록 해야함
    context = {
        "user_position": user_position,
        # "user_coords": user_current_coords.lstrip("[").rstrip("]").replace("'", ""),
    }
    return render(request, "articles/locations.html", context)

    # 마커, 현재위치버튼

    # DB 가져올 수 있게 저장하기
    # 현재위치 요청에서 가져오기
    # 초기화면 로드 오류 fix


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


def songlike(request, pk):

    song = Song.objects.get(pk=pk)

    # if request.user in song.like_users.all():
    #     song.like_users.remove(request.user)
    # else:
    #     song.like_users.add(request.user)

    # return redirect("articles:private")

    if song.like_users.filter(pk=request.user.pk).exists():
        song.like_users.remove(request.user)
        is_liked = False
    else:
        song.like_users.add(request.user)
        is_liked = True

    songlike_count = song.like_users.count()

    context = {
        "is_liked": is_liked,
        "likeCount": songlike_count,
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
    comment_form = CommentForm(request.POST)
    context = {
        "song": song,
        "articles": articles,
        "comment_form": comment_form,
    }
    return render(request, "articles/song_detail.html", context)


@login_required
def song_like(request, pk):

    song = Song.objects.get(pk=pk)

    if song.like_users.filter(pk=request.user.pk).exists():
        song.like_users.remove(request.user)
        is_liked = False
    else:
        song.like_users.add(request.user)
        is_liked = True

    like_count = song.like_users.count()

    context = {
        "is_liked": is_liked,
        "likeCount": like_count,
    }
    return JsonResponse(context)


@login_required
def create_test(request):
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
            new_article = Article.objects.create(
                user=request.user,
                place=place,
                content=content,
                song=song,
            )
            return redirect("articles:detail", new_article.pk)
        else:
            return redirect("articles:create_test")
    return render(request, "articles/create_test.html")
