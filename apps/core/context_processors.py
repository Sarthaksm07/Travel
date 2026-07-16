from .models import SiteConfig


def site(request):
    """Expose site-wide config (phone, whatsapp, address, socials) to all templates."""
    try:
        return {"site": SiteConfig.load()}
    except Exception:
        # Before the first migration the table may not exist yet.
        return {"site": None}
