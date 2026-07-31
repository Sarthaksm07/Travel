from django.shortcuts import get_object_or_404, render

from .models import PackageCategory, TourPackage


def package_list(request):
    packages = TourPackage.objects.all()
    categories = PackageCategory.objects.filter(packages__isnull=False).distinct()
    return render(
        request,
        "pages/packages.html",
        {"packages": packages, "categories": categories},
    )


def package_detail(request, slug):
    # Strict: an unknown/renamed slug returns a proper 404.
    package = get_object_or_404(TourPackage, slug=slug)
    qs = TourPackage.objects.exclude(pk=package.pk)
    if package.category_id:
        qs = qs.filter(category=package.category)
    related = qs[:3]
    return render(
        request,
        "pages/package-detail.html",
        {"package": package, "related": related},
    )
