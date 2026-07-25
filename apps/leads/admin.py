from django.contrib import admin

from .models import Inquiry, NewsletterSubscriber


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    """The lead view — read-mostly, with editable follow-up status."""

    list_display = ("name", "phone", "destination", "num_travellers", "source_type", "follow_up_status", "created_at")
    list_filter = ("follow_up_status", "source_type", "created_at")
    search_fields = ("name", "phone", "email", "message", "destination")
    list_editable = ("follow_up_status",)
    date_hierarchy = "created_at"
    readonly_fields = (
        "name", "phone", "email", "destination", "num_travellers", "num_kids",
        "travel_date", "vehicle_preference", "hotel_category", "message",
        "source_type", "related_package", "created_at",
    )

    def has_add_permission(self, request):
        return False


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at")
    search_fields = ("email",)
