from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "articles/index.html")


def location_get(request):
    user_location = request.session.get("userLocation", "none")
    context = {
        "userLocation": user_location,
    }
    return render(request, "articles/locations.html", context)
