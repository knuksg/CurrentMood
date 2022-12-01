from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = ("user",)
        labels = {
            "title": "사연 제목",
            "content": "사연 내용",
            "place": "사연 장소",
            "song": "노래 제목",
            "singer": "가수",
            "image": "이미지",
        }
