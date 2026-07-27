from django.shortcuts import render

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
    # Non-strict: fall back to the static sample if the package isn't in the DB yet.
    package = TourPackage.objects.filter(slug=slug).first()
    related = None
    if package:
        qs = TourPackage.objects.exclude(pk=package.pk)
        if package.category_id:
            qs = qs.filter(category=package.category)
        related = qs[:3]
    return render(
        request,
        "pages/package-detail.html",
        {"package": package, "related": related},
    )
