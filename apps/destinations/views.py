from django.shortcuts import get_object_or_404, render

from .models import Destination


def destination_list(request):
    return render(request, "pages/destinations.html", {
        "destinations": Destination.objects.all(),
    })


def destination_detail(request, slug):
    # Strict: an unknown/renamed slug returns a proper 404.
    destination = get_object_or_404(Destination, slug=slug)
    return render(request, "pages/destination-detail.html", {
        "destination": destination,
        "packages": destination.packages.all(),
        "faqs": destination.faqs.filter(is_active=True),
        "gallery": destination.images.all(),
    })
