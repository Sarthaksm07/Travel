from django.shortcuts import render

from tours.models import TourPackage


def home(request):
    context = {
        # Packages ticked "is featured" in the admin, newest first.
        "featured_packages": TourPackage.objects.filter(is_featured=True)[:8],
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")
