from django.shortcuts import render


def home(request):
    """Home page – all UI lives in pages app."""
    return render(request, "pages/home.html")
