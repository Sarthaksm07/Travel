from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "location", "rating", "is_approved", "is_featured", "order")
    list_editable = ("is_approved", "is_featured", "order")
    list_filter = ("is_approved", "is_featured", "rating")
    search_fields = ("customer_name", "text")
    actions = ["approve_selected", "unapprove_selected"]

    @admin.action(description="Approve selected testimonials")
    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Unapprove selected testimonials")
    def unapprove_selected(self, request, queryset):
        queryset.update(is_approved=False)
