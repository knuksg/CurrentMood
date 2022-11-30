from django.shortcuts import render, redirect
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):

    users = User.objects.all()

    context = {
        "users": users,
    }

    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "accounts:index")
    else:
        form = AuthenticationForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect("accounts:index")


@login_required
def update(request, pk):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:mypage")
    else:
        form = CustomUserChangeForm(instance=request.user)
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

    return redirect("accounts:index")


@login_required
def follow(request, pk):

    if request.user.pk != pk:
        user = get_user_model().objects.get(pk=pk)

        if request.user in user.followers.all():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)

        return redirect("accounts:detail", pk)
    else:
        return redirect("base:base")


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
def my_followlist(request, pk):

    user = get_user_model().objects.get(pk=pk)

    context = {
        "user": user,
    }
    return render(request, "accounts/my_followlist.html", context)


@login_required
def my_followerlist(request, pk):

    user = get_user_model().objects.get(pk=pk)

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
