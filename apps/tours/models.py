from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class PackageCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Package categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TourPackage(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        PackageCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages",
    )
    destinations = models.ManyToManyField(
        "destinations.Destination", blank=True, related_name="packages"
    )

    short_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    duration = models.CharField(
        max_length=60, blank=True, help_text='e.g. "6 Days / 5 Nights"'
    )

    itinerary = CKEditor5Field("Itinerary", config_name="extends", blank=True)
    inclusions = CKEditor5Field("Inclusions", config_name="extends", blank=True)
    exclusions = CKEditor5Field("Exclusions", config_name="extends", blank=True)
    accommodation_details = CKEditor5Field("Accommodation", config_name="extends", blank=True)
    transport_details = CKEditor5Field("Transport", config_name="extends", blank=True)
    terms_and_conditions = CKEditor5Field("Terms & conditions", config_name="extends", blank=True)

    cover_image = models.ImageField(upload_to="packages/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PackageImage(models.Model):
    package = models.ForeignKey(
        TourPackage, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="packages/gallery/")
    caption = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Image #{self.pk}"
