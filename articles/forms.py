from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = (
            "user",
            "like_users",
            "song",
        )
        labels = {
            "title": "사연 제목",
            "content": "사연 내용",
            "place": "사연 장소",
            "song": "노래 제목",
            "singer": "가수",
            "image": "이미지",
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "댓글을 남겨주세요.",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["content"]
