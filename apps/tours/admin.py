from django.contrib import admin

from core.models import FAQ

from .models import PackageCategory, PackageImage, TourPackage


class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1


class PackageFAQInline(admin.TabularInline):
    model = FAQ
    fk_name = "package"
    exclude = ("destination",)
    extra = 1


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "duration", "is_featured", "is_seasonal", "order")
    list_editable = ("is_featured", "is_seasonal", "order")
    list_filter = ("category", "is_featured", "is_seasonal")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("destinations",)
    inlines = [PackageImageInline, PackageFAQInline]


@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
