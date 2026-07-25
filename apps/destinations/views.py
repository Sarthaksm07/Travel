from django.shortcuts import render

from .models import Destination


def destination_list(request):
    return render(request, "pages/destinations.html", {
        "destinations": Destination.objects.all(),
    })


def destination_detail(request, slug):
    # Non-strict: if the destination isn't in the DB yet, the template falls
    # back to the static sample so links never break during content entry.
    destination = Destination.objects.filter(slug=slug).first()
    context = {"destination": destination}
    if destination:
        context["packages"] = destination.packages.all()
        context["faqs"] = destination.faqs.filter(is_active=True)
        context["gallery"] = destination.images.all()
    return render(request, "pages/destination-detail.html", context)
