from django.db import models


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")
    text = models.TextField()
    video_url = models.URLField(blank=True)
    is_approved = models.BooleanField(
        default=False, help_text="Unapproved testimonials never appear on the public site."
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"
