from django.shortcuts import render, redirect
from .models import *
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from main.models import Song
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

# 위치 api 구현
from .gmap import reverse_geocoding, parsing_geocoded
import requests
import os
import pprint
import json

# Create your views here.
def private(request):
    articles = Article.objects.filter(place="블루보틀")
    comment_form = CommentForm()
    context = {
        "articles": articles,
        "comment_form": comment_form,
    }
    return render(request, "articles/private.html", context)


def index(request):
    articles = Article.objects.all().order_by("-pk")
    context = {
        "articles": articles,
    }
    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        place = request.POST.get('place', '')
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        vidid = request.POST.get('vidid', '')
        vidtitle = request.POST.get('vidtitle', '')
        channel = request.POST.get('channel', '')
        hqdefault = request.POST.get('hqdefault', '')
        default = request.POST.get('default', '')
        mqdefault = request.POST.get('mqdefault', '')
        try:
            song = Song.objects.get(vidid=vidid)
        except:
            song = Song.objects.create(vidid=vidid, title=vidtitle, channel=channel, hqdefault=hqdefault, default=default, mqdefault=mqdefault)
        Article.objects.create(
            user = request.user,
            place = place,
            title = title,
            content = content,
            song = song,
        )
        return redirect("articles:index")
    else:
        form = ArticleForm()
    context = {
        "form": form,
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
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect("articles:detail", article.pk)
    else:
        form = ArticleForm(instance=article)

    context = {
        "form": form,
    }
    return render(request, "articles/update.html", context)


def location_get(request):
    # 위치 정보 가져오기 : google geolocation api 요청
    gmap_api_key = os.getenv("gmap_api")
    print(request.POST.get("userLocation"))
    if request.method == "POST":
        user_coords = request.POST.get("userLocation").split(",")
        coords = user_coords
        user_loc = parsing_geocoded(coords[0], coords[1])["user_loc"]
    else:
        user_loc = ["somewhere"]
    # Place 테이블에 geocoding된 위치 값을 저장한다.
    for i in user_loc:
        place_location = Place.objects.create(name=i)
    # user가 있는 경우
    ###
    context = {
        "user_position": user_loc[0],
        "key": gmap_api_key,
    }
    return render(request, "articles/locations.html", context)


def public(request):
    # place model에서 필드를 가져온다.
    place = Place.objects.all()
    context = {
        "place": place,
    }
    return render(request, "articles/public.html", context)


def test(request):
    return render(request, "articles/test.html")


@login_required
def like(request, pk):

    article = Article.objects.get(pk=pk)

    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)

    return redirect("articles:detail", pk)


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
