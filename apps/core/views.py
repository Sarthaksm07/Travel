from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from blog.models import BlogPost
from destinations.models import Destination
from testimonials.models import Testimonial
from tours.models import TourPackage

from .models import GalleryCategory, GalleryImage, SiteConfig, SitePage, Stat, Vehicle


def home(request):
    posts = list(BlogPost.objects.filter(published=True)[:4])
    cheapest = (
        Vehicle.objects.filter(is_active=True, per_km_rate__isnull=False)
        .order_by("per_km_rate")
        .first()
    )
    cfg = SiteConfig.load()
    title, hl = cfg.hero_title or "", cfg.hero_highlight or ""
    if hl and hl in title:
        hero_before, hero_after = title.split(hl, 1)
    else:
        hero_before, hl, hero_after = title, "", ""

    context = {
        "hero_before": hero_before,
        "hero_highlight_word": hl,
        "hero_after": hero_after,
        "featured_packages": TourPackage.objects.filter(is_featured=True)[:8],
        "featured_destinations": Destination.objects.filter(is_featured=True)[:8],
        "all_destinations": Destination.objects.all(),
        "stats": Stat.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_approved=True)[:6],
        "latest_posts": posts[:3],
        "vehicle_from_rate": cheapest.per_km_rate if cheapest else None,
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html", {
        "stats": Stat.objects.filter(is_active=True),
    })


def contact(request):
    return render(request, "pages/contact.html")


def thank_you(request):
    return render(request, "pages/thank-you.html")


def vehicles(request):
    return render(request, "pages/vehicles.html", {
        "vehicles": Vehicle.objects.filter(is_active=True),
    })


def gallery(request):
    return render(request, "pages/gallery.html", {
        "images": GalleryImage.objects.filter(is_active=True).select_related("category"),
        "categories": GalleryCategory.objects.filter(images__is_active=True).distinct(),
    })


def page(request, slug):
    """Render an admin-managed static page (Privacy, Terms, etc.)."""
    obj = SitePage.objects.filter(slug=slug).first()
    return render(request, "pages/legal.html", {"page": obj, "slug": slug})


def search(request):
    q = request.GET.get("q", "").strip()
    packages = destinations = []
    if q:
        # Match on names/titles + category (predictable), not long body text.
        packages = TourPackage.objects.filter(
            Q(title__icontains=q) | Q(category__name__icontains=q)
        ).distinct()
        destinations = Destination.objects.filter(name__icontains=q).distinct()
    return render(request, "pages/search.html", {
        "q": q,
        "packages": packages,
        "destinations": destinations,
        "total": len(packages) + len(destinations),
    })


def search_suggest(request):
    """Live autocomplete: name/title matches as JSON."""
    q = request.GET.get("q", "").strip()
    results = []
    if q:
        for p in TourPackage.objects.filter(
            Q(title__icontains=q) | Q(category__name__icontains=q)
        ).distinct()[:6]:
            results.append({
                "label": p.title, "type": "Package",
                "url": reverse("tours:detail", args=[p.slug]),
            })
        for d in Destination.objects.filter(name__icontains=q)[:6]:
            results.append({
                "label": d.name, "type": "Destination",
                "url": reverse("destinations:detail", args=[d.slug]),
            })
    return JsonResponse({"results": results})
