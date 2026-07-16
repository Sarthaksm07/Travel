from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class SiteConfig(models.Model):
    """Single-row site-wide configuration, editable in admin. Use SiteConfig.load()."""

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
