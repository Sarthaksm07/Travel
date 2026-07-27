from django.shortcuts import render

from blog.models import BlogPost
from destinations.models import Destination
from testimonials.models import Testimonial
from tours.models import TourPackage

from .models import Vehicle


def home(request):
    posts = list(BlogPost.objects.filter(published=True)[:4])
    cheapest = (
        Vehicle.objects.filter(is_active=True, per_km_rate__isnull=False)
        .order_by("per_km_rate")
        .first()
    )
    context = {
        "featured_packages": TourPackage.objects.filter(is_featured=True)[:8],
        "featured_destinations": Destination.objects.filter(is_featured=True)[:8],
        "all_destinations": Destination.objects.all(),
        "testimonials": Testimonial.objects.filter(is_approved=True)[:6],
        "latest_posts": posts[:3],
        "vehicle_from_rate": cheapest.per_km_rate if cheapest else None,
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")


def thank_you(request):
    return render(request, "pages/thank-you.html")


def vehicles(request):
    return render(request, "pages/vehicles.html", {
        "vehicles": Vehicle.objects.filter(is_active=True),
    })
