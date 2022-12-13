from django.shortcuts import render, redirect
from .models import User
from articles import models
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from main.models import Song
from django.http import JsonResponse

# Create your views here.


def index(request):

    users = User.objects.all()

    context = {
        "users": users,
    }

    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        print(1)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # print(2)
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()
        # print(3)
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "articles:private")
    else:
        form = AuthenticationForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect("articles:private")


@login_required
def update(request, pk):
    user = get_user_model().objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:mypage")
    else:
        form = CustomUserChangeForm(instance=user)
    context = {"form": form}

    return render(request, "accounts/update.html", context)


@login_required
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)


@login_required
def mypage(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/mypage.html", context)


@login_required
def delete(request):

    request.user.delete()
    auth_logout(request)

    return redirect("articles:private")


@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)
    me = get_user_model().objects.get(pk=request.user.pk)
    if request.user.pk != pk:
        if request.user not in user.followers.all():
            request.user.followings.add(user)
            is_follow = True
        else:
            request.user.followings.remove(user)
            is_follow = False
        context = {
            "isFollow": is_follow,
            "followers_count": user.followers.count(),
            "followings_count": user.followings.count(),
            "myfollowings_count": me.followings.count(),
        }
        return JsonResponse(context)


@login_required
def followlist(request, pk):

    user = get_user_model().objects.get(pk=pk)

    context = {
        "user": user,
    }
    return render(request, "accounts/followlist.html", context)


@login_required
def followerlist(request, pk):

    user = get_user_model().objects.get(pk=pk)

    context = {
        "user": user,
    }
    return render(request, "accounts/followerlist.html", context)


@login_required
def my_followlist(request):

    user = get_user_model().objects.get(pk=request.user.pk)

    context = {
        "user": user,
    }
    return render(request, "accounts/my_followlist.html", context)


@login_required
def my_followerlist(request):

    user = get_user_model().objects.get(pk=request.user.pk)

    context = {
        "user": user,
    }
    return render(request, "accounts/my_followerlist.html", context)


@login_required
def password(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호가 성공적으로 변경되었습니다.")
            return redirect("accounts:login")
        else:
            messages.error(request, "비밀번호 변경에 실패하였습니다.")
    else:
        form = PasswordChangeForm(request.user)

    context = {
        "form": form,
    }
    return render(request, "accounts/password.html", context)


def popular(request):

    users = User.objects.order_by("-followers")

    context = {
        "users": users,
    }

    return render(request, "accounts/popular.html", context)


@login_required
def my_sharedmusiclist(request):

    return render(request, "accounts/my_sharedmusiclist.html")


@login_required
def my_likedmusiclist(request):

    articles = request.user.like_article.all()
    articles = articles.order_by("-pk")

    context = {
        "articles": articles,
    }

    return render(request, "accounts/my_likedmusiclist.html", context)


def profile_music(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        vidid = request.POST.get("vidid", "")
        title = request.POST.get("title", "")
        channel = request.POST.get("channel", "")
        hqdefault = request.POST.get("hqdefault", "")
        default = request.POST.get("default", "")
        mqdefault = request.POST.get("mqdefault", "")
        try:
            song = Song.objects.get(vidid=vidid)
            user.profile_music = song
            user.save(update_fields=["profile_music"])
        except:
            song = Song.objects.create(
                vidid=vidid,
                title=title,
                channel=channel,
                hqdefault=hqdefault,
                default=default,
                mqdefault=mqdefault,
            )
            user.profile_music = song
            user.save(update_fields=["profile_music"])
    return render(request, "accounts/profile_music.html")


@login_required
def mylist(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/mylist.html", context)


@login_required
def profile_music_delete(request, pk):
    user = get_user_model().objects.get(pk=pk)
    user.profile_music = None
    user.save(update_fields=["profile_music"])
    context = {
        "user": user,
    }
    return redirect("accounts:mypage")


@login_required
def playlist(request):
    context = {}
    return render(request, "accounts/playlist.html", context)
