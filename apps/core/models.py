from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class SiteConfig(models.Model):
    """Single-row site-wide configuration, editable in admin. Use SiteConfig.load()."""

    logo = models.ImageField(
        upload_to="site/", blank=True, null=True,
        validators=[FileExtensionValidator(["png"])],
        help_text="PNG only. Shows in the navbar and footer. Leave blank to use the default logo.",
    )

    # --- Homepage hero banner (all editable here) ---
    hero_eyebrow = models.CharField(max_length=80, default="Devbhoomi Uttarakhand", blank=True)
    hero_title = models.CharField(
        max_length=160, default="Journeys to the sacred Himalayas.",
        help_text="Main headline.",
    )
    hero_highlight = models.CharField(
        max_length=60, default="sacred", blank=True,
        help_text="A word/phrase inside the title to emphasise (clay italic). Must appear in the title.",
    )
    hero_subtitle = models.TextField(
        default="Safe, women-friendly, transparently priced pilgrimages and mountain "
                "tours — crafted by local experts who live in the valleys of Kedarnath.",
        blank=True,
    )
    hero_image = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text="Hero banner image. Leave blank to use the default.",
    )
    hero_badge = models.CharField(max_length=60, default="Kedarnath · Badrinath", blank=True,
                                  help_text="Small pill on the image corner. Leave blank to hide.")
    hero_stat_value = models.CharField(max_length=30, default="15+ yrs", blank=True)
    hero_stat_label = models.CharField(max_length=80, default="Guiding the Char Dham route", blank=True)
    hero_rating = models.CharField(max_length=60, default="4.8 · 6000+ travellers", blank=True,
                                   help_text="Rating line under the buttons. Leave blank to hide.")
    hero_primary_label = models.CharField(max_length=40, default="Explore Packages",
                                          help_text="Left button (links to Packages).")
    hero_secondary_label = models.CharField(max_length=40, default="Plan Your Journey",
                                            help_text="Right button (links to the enquiry form).")

    phone = models.CharField(max_length=40, default="+91 8630 731 034")
    whatsapp_number = models.CharField(
        max_length=40,
        default="918630731034",
        help_text="International format, no '+' or spaces, e.g. 918630731034",
    )
    email = models.EmailField(default="augytravels@gmail.com")
    address = models.CharField(
        max_length=255,
        default="Bedubagarh, Kedarnath Road, Rudraprayag, Uttarakhand 246421",
    )
    google_maps_link = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SitePage(models.Model):
    """Editable static content (e.g. About) managed from admin."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    body = CKEditor5Field("Body", config_name="extends", blank=True)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Stat(models.Model):
    """A headline stat shown in the homepage trust strip (editable in admin)."""

    ICON_CHOICES = [
        ("fas fa-users", "People / Travellers"),
        ("fas fa-star", "Star / Rating"),
        ("fas fa-mountain-sun", "Mountain"),
        ("fas fa-shield-heart", "Shield (safety)"),
        ("fas fa-route", "Route"),
        ("fas fa-award", "Award / Badge"),
        ("fas fa-calendar-check", "Calendar"),
        ("fas fa-map-location-dot", "Map"),
        ("fas fa-car-side", "Vehicle"),
        ("fas fa-headset", "Support"),
        ("fas fa-thumbs-up", "Thumbs up"),
        ("fas fa-heart", "Heart"),
        ("fas fa-earth-asia", "Globe"),
        ("fas fa-hotel", "Hotel"),
        ("fas fa-person-hiking", "Hiking"),
    ]

    value = models.CharField(max_length=20, help_text='e.g. "6000+", "4.8", "100%"')
    label = models.CharField(max_length=60, help_text='e.g. "Happy Travellers"')
    icon = models.CharField(
        max_length=40, choices=ICON_CHOICES, default="fas fa-star",
        help_text="Pick an icon from the list",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} — {self.label}"


class GalleryCategory(models.Model):
    """An album / trip grouping for gallery photos (e.g. 'Auli & Chopta Tour')."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Gallery categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    """A photo for the site-wide Travel Experiences gallery."""

    title = models.CharField(max_length=150, blank=True, help_text="Optional caption/location")
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="images", help_text="Album / trip this photo belongs to",
    )
    image = models.ImageField(upload_to="gallery/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title or f"Photo #{self.pk}"


class Vehicle(models.Model):
    """A rentable, chauffeur-driven vehicle shown on the Rentals page."""

    name = models.CharField(max_length=120, help_text='e.g. "Swift / Aura"')
    category = models.CharField(max_length=80, blank=True, help_text='e.g. "Sedan", "Premium SUV"')
    seating = models.CharField(max_length=40, blank=True, help_text='e.g. "4 seats", "12–26 seats"')
    per_km_rate = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=True,
        help_text="Indicative per-km rate with driver, in ₹",
    )
    best_for = models.CharField(max_length=180, blank=True, help_text="Short one-line description")
    icon = models.CharField(
        max_length=40, default="fas fa-car",
        help_text="Font Awesome class, used when no image is uploaded",
    )
    image = models.ImageField(upload_to="vehicles/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "per_km_rate"]

    def __str__(self):
        return self.name


class FAQ(models.Model):
    """Shared FAQ. Attach to a destination or a package, or leave both blank for a general FAQ."""

    question = models.CharField(max_length=255)
    answer = models.TextField()
    destination = models.ForeignKey(
        "destinations.Destination",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="faqs",
    )
    package = models.ForeignKey(
        "tours.TourPackage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="faqs",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question

    @property
    def scope(self):
        if self.destination_id:
            return "Destination"
        if self.package_id:
            return "Package"
        return "General"
