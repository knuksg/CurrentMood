from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("delete/", views.delete, name="delete"),
    path("password/", views.password, name="password"),
    path("popular/", views.popular, name="popular"),
    path("mypage/", views.mypage, name="mypage"),
    path("mypage/followlist/", views.my_followlist, name="my_followlist"),
    path("mypage/followerlist/", views.my_followerlist, name="my_followerlist"),
    path(
        "mypage/profile_music/<int:pk>/", views.profile_music, name="profile_music"
    ),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("<int:pk>/followlist/", views.followlist, name="followlist"),
    path("<int:pk>/followerlist/", views.followerlist, name="followerlist"),
]
