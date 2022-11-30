from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request, "main/base.html")
    
def test(request):
    return render(request, "main/test.html")

def test2(request):
    return render(request, "main/test2.html")