from django.shortcuts import render, redirect
from .models import Song

# Create your views here.


def base(request):
    return render(request, "main/base.html")


def test(request):
    return render(request, "main/test.html")


def test2(request):
    return render(request, "main/test2.html")


def test3(request):
    return render(request, "main/test3.html")
