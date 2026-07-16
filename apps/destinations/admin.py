from django.contrib import admin

from core.models import FAQ

from .models import Destination, DestinationImage


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1


class DestinationFAQInline(admin.TabularInline):
    model = FAQ
    fk_name = "destination"
    exclude = ("package",)
    extra = 1


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_featured", "order", "created_at")
    list_editable = ("is_featured", "order")
    search_fields = ("name", "overview")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [DestinationImageInline, DestinationFAQInline]
