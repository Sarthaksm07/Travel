from django.contrib import admin

from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    """The lead view — read-mostly, with editable follow-up status."""

    list_display = ("name", "phone", "source_type", "related_package", "follow_up_status", "created_at")
    list_filter = ("follow_up_status", "source_type", "created_at")
    search_fields = ("name", "phone", "email", "message")
    list_editable = ("follow_up_status",)
    date_hierarchy = "created_at"
    readonly_fields = ("name", "phone", "email", "message", "source_type", "related_package", "created_at")

    def has_add_permission(self, request):
        # Leads are created from public forms, not typed in admin.
        return False
