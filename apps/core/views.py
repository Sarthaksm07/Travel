from django.shortcuts import render

from blog.models import BlogPost
from destinations.models import Destination
from testimonials.models import Testimonial
from tours.models import TourPackage


def home(request):
    posts = list(BlogPost.objects.filter(published=True)[:4])
    context = {
        "featured_packages": TourPackage.objects.filter(is_featured=True)[:8],
        "featured_destinations": Destination.objects.filter(is_featured=True)[:8],
        "testimonials": Testimonial.objects.filter(is_approved=True)[:6],
        "latest_post": posts[0] if posts else None,
        "recent_posts": posts[1:4],
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")


def thank_you(request):
    return render(request, "pages/thank-you.html")


def vehicles(request):
    return render(request, "pages/vehicles.html")
