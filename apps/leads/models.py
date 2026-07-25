from django.db import models


class Inquiry(models.Model):
    class SourceType(models.TextChoices):
        GENERAL = "general", "General"
        PACKAGE = "package", "Package"
        BOOKING = "booking", "Booking request"
        CUSTOM_TOUR = "custom-tour", "Custom tour"
        CALLBACK = "callback", "Callback"
        WHATSAPP = "whatsapp", "WhatsApp"

    class FollowUp(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)

    # Booking-request details (optional — used by the Plan Your Trip form)
    destination = models.CharField(max_length=150, blank=True)
    num_travellers = models.PositiveIntegerField(null=True, blank=True, verbose_name="No. of travellers")
    num_kids = models.PositiveIntegerField(null=True, blank=True, verbose_name="No. of kids (below 5)")
    travel_date = models.DateField(null=True, blank=True)
    vehicle_preference = models.CharField(max_length=40, blank=True)
    hotel_category = models.CharField(max_length=40, blank=True)

    source_type = models.CharField(
        max_length=20, choices=SourceType.choices, default=SourceType.GENERAL
    )
    related_package = models.ForeignKey(
        "tours.TourPackage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries",
    )
    follow_up_status = models.CharField(
        max_length=20, choices=FollowUp.choices, default=FollowUp.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.name} — {self.get_source_type_display()} ({self.created_at:%d %b %Y})"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
