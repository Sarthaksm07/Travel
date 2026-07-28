from .models import SiteConfig


def site(request):
    """Expose site-wide config + footer data to all templates."""
    try:
        cfg = SiteConfig.load()
    except Exception:
        # Before the first migration the table may not exist yet.
        return {"site": None, "footer_packages": []}

    footer_packages = []
    try:
        from tours.models import TourPackage
        qs = TourPackage.objects.filter(is_featured=True)[:5]
        if not qs:
            qs = TourPackage.objects.all()[:5]
        footer_packages = list(qs)
    except Exception:
        pass

    return {"site": cfg, "footer_packages": footer_packages}
