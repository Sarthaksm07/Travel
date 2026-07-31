from django.contrib import admin

from .models import (
    FAQ, GalleryCategory, GalleryImage, SiteConfig, SitePage, Stat, Vehicle,
)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("logo",)}),
        ("Homepage hero banner", {
            "fields": (
                "hero_eyebrow", "hero_title", "hero_highlight", "hero_subtitle",
                "hero_image", "hero_badge", "hero_stat_value", "hero_stat_label",
                "hero_rating", "hero_primary_label", "hero_secondary_label",
            ),
        }),
        ("Contact details", {"fields": ("phone", "whatsapp_number", "email", "address", "google_maps_link")}),
        ("Social links", {"fields": ("facebook_url", "instagram_url", "youtube_url")}),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "body")


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "icon", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "order", "is_active", "created_at")
    list_editable = ("category", "order", "is_active")
    list_filter = ("is_active", "category")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "seating", "per_km_rate", "is_active", "order")
    list_editable = ("per_km_rate", "is_active", "order")
    list_filter = ("is_active", "category")
    search_fields = ("name", "category")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "scope", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("question", "answer")
