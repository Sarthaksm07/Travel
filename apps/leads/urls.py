from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("", views.booking, name="booking"),
    path("query/", views.quick_query, name="query"),
    path("callback/", views.callback, name="callback"),
    path("contact/", views.contact, name="contact"),
]
