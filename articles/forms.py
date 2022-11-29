from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = ("user",)
        labels = {
            "title": "제목",
            "content": "내용",
            "image": "이미지",
        }
