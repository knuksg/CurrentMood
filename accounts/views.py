from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "accounts/index.html")


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
            return redirect("accounts:detail", pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}

    return render(request, "accounts/update.html", context)


@login_required
def detail(request, pk):

    if request.user.pk == pk:
        user = get_user_model().objects.get(pk=pk)
        context = {
            "user": user,
        }
        return render(request, "accounts/detail.html", context)
    else:
        return redirect("accounts:index")


@login_required
def delete(request):

    request.user.delete()
    auth_logout(request)

    return redirect("accounts:index")
