from django.shortcuts import render


def package_list(request):
    return render(request, "pages/packages.html")


def package_detail(request, slug):
    # Static for now — one template serves as the sample for every package.
    # When we go dynamic:
    #   package = get_object_or_404(TourPackage, slug=slug)
    #   return render(request, "pages/package-detail.html", {"package": package})
    return render(request, "pages/package-detail.html")
