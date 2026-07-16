from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class Destination(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    overview = CKEditor5Field("Overview", config_name="extends", blank=True)
    attractions = CKEditor5Field("Attractions", config_name="extends", blank=True)
    travel_guide = CKEditor5Field("Travel guide", config_name="extends", blank=True)
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    local_activities = CKEditor5Field("Local activities", config_name="extends", blank=True)
    cover_image = models.ImageField(upload_to="destinations/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DestinationImage(models.Model):
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="destinations/gallery/")
    caption = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Image #{self.pk}"
