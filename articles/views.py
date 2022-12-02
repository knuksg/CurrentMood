from django.shortcuts import render, redirect
from .models import Article, Place
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required

# 위치 api 구현
from .gmap import geocoding
from .place_choose import choose_location
import requests
import os
import pprint
import json

# Create your views here.
def private(request):
    return render(request, "articles/private.html")


def index(request):
    articles = Article.objects.all().order_by("-pk")
    context = {
        "articles": articles,
    }
    return render(request, "articles/index.html", context)


def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect("articles:index")
    else:
        form = ArticleForm()
    context = {
        "form": form,
    }
    return render(request, "articles/create.html", context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        "article": article,
    }
    return render(request, "articles/detail.html", context)


def delete(request, pk):
    Article.objects.get(pk=pk).delete()
    return redirect("articles:index")


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
    print(request.POST.get("userLocation"))
    # 위치 정보 가져오기 : google geolocation api 요청
    # mac wifi주소를 가져올 수 없는 경우, web geolocation api 정확도가 더 높다.
    gmap_api_key = os.getenv("gmap_api")
    # 예시 위치
    location = requests.post(
        f"https://www.googleapis.com/geolocation/v1/geolocate?key={gmap_api_key}",
        json={
            "considerIp": "true",
            "wifiAccessPoints": [
                {
                    "macAddress": "84:d4:7e:f6:99:64",
                    "signalStrength": -54,
                    "signalToNoiseRatio": 0,
                },
                {
                    "macAddress": "84:d4:7e:f6:99:71",
                    "signalStrength": -43,
                    "signalToNoiseRatio": 0,
                },
                {
                    "macAddress": "84:d4:7e:f7:21:35",
                    "signalStrength": -32,
                    "signalToNoiseRatio": 0,
                },
            ],
        },
    ).json()
    coords = location["location"]
    # user가 없는 경우 : 먼 거리의 장소를 보여준다.
    user_loc = choose_location(coords["lat"], coords["lng"])["user_loc"]
    geocoded = choose_location(coords["lat"], coords["lng"])["geocoded"]
    # Place 테이블에 geocoding된 위치 값을 저장한다.
    for i in user_loc:
        place_location = Place.objects.create(name=i)
    # user가 있는 경우
    ###
    context = {
        "geocoded": geocoded,
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
