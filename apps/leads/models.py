from django.db import models


class Inquiry(models.Model):
    class SourceType(models.TextChoices):
        GENERAL = "general", "General"
        PACKAGE = "package", "Package"
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
