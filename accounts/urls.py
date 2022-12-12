from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
        "mypage/sharedmusiclist/", views.my_sharedmusiclist, name="my_sharedmusiclist"
    ),
    path("mypage/profile_music/<int:pk>/", views.profile_music, name="profile_music"),
    path(
        "mypage/profile_music/<int:pk>/delete",
        views.profile_music_delete,
        name="profile_music_delete",
    ),
    path("mypage/likedmusiclist/", views.my_likedmusiclist, name="my_likedmusiclist"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("<int:pk>/followlist/", views.followlist, name="followlist"),
    path("<int:pk>/followerlist/", views.followerlist, name="followerlist"),
    path("mylist/", views.mylist, name="mylist"),
    path("playlist/", views.playlist, name="playlist"),
]
