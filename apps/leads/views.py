import re

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from destinations.models import Destination
from tours.models import TourPackage

from .models import Inquiry


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def booking(request):
    if request.method == "POST":
        d = request.POST
        is_rental = d.get("source", "").strip() == "rental"
        pkg = None
        pkg_slug = d.get("package", "").strip()
        if pkg_slug:
            pkg = TourPackage.objects.filter(slug=pkg_slug).first()
        if is_rental:
            source = Inquiry.SourceType.RENTAL
        elif pkg:
            source = Inquiry.SourceType.PACKAGE
        else:
            source = Inquiry.SourceType.BOOKING
        inq = Inquiry.objects.create(
            name=d.get("name", "").strip(),
            phone=d.get("phone", "").strip(),
            email=d.get("email", "").strip(),
            destination=d.get("destination", "").strip(),
            num_travellers=_to_int(d.get("num_travellers")),
            num_kids=_to_int(d.get("num_kids")),
            travel_date=parse_date(d.get("travel_date") or "") or None,
            vehicle_preference=d.get("vehicle_preference", "").strip(),
            hotel_category=d.get("hotel_category", "").strip(),
            message=d.get("message", "").strip(),
            related_package=pkg,
            source_type=source,
        )
        label = "rental enquiry" if is_rental else ("package enquiry" if pkg else "trip request")
        body = "\n".join([
            f"New {label} from {inq.name}",
            "",
            f"Phone:        {inq.phone}",
            f"Email:        {inq.email or '-'}",
            f"Package:      {pkg.title if pkg else '-'}",
            f"Destination:  {inq.destination or '-'}",
            f"Travellers:   {inq.num_travellers or '-'}",
            f"Kids (<5):    {inq.num_kids or '-'}",
            f"Travel date:  {inq.travel_date or '-'}",
            f"Vehicle:      {inq.vehicle_preference or '-'}",
            f"Hotel:        {inq.hotel_category or '-'}",
            f"Message:      {inq.message or '-'}",
        ])
        send_mail(
            subject=f"New {label} — {inq.name}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.LEADS_NOTIFY_EMAIL],
            fail_silently=True,
        )
        return redirect("core:thank_you")

    # Pre-fill from the homepage enquiry bar (or vehicle "Book" links).
    # Each value maps 1:1 into its own structured field on the form.
    g = request.GET
    prefill_package = None
    prefill_destination = g.get("destination", "").strip()
    pkg_slug = g.get("package", "").strip()
    if pkg_slug:
        prefill_package = TourPackage.objects.filter(slug=pkg_slug).first()
        if prefill_package and not prefill_destination:
            first_dest = prefill_package.destinations.first()
            if first_dest:
                prefill_destination = first_dest.name
    return render(request, "pages/booking.html", {
        "prefill_vehicle": g.get("vehicle", "").strip(),
        "is_rental": g.get("source", "").strip() == "rental",
        "prefill_package": prefill_package,
        "prefill_destination": prefill_destination,
        "prefill_travel_date": g.get("travel_date", "").strip(),
        "prefill_travellers": g.get("num_travellers", "").strip(),
        "dest_names": list(Destination.objects.values_list("name", flat=True)),
    })


@require_POST
def contact(request):
    """Contact-page enquiry — saves a lead, emails Augy, then thank-you page."""
    d = request.POST
    email = d.get("email", "").strip()
    # If an email is given, it must be a complete address (name@domain.tld).
    if email and not re.match(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$", email):
        return redirect("core:contact")
    inq = Inquiry.objects.create(
        name=d.get("name", "").strip() or "Website visitor",
        phone=d.get("phone", "").strip(),
        email=email,
        destination=d.get("destination", "").strip(),
        message=d.get("message", "").strip(),
        source_type=Inquiry.SourceType.GENERAL,
    )
    body = "\n".join([
        f"New contact enquiry from {inq.name}",
        "",
        f"Phone:        {inq.phone}",
        f"Email:        {inq.email or '-'}",
        f"Destination:  {inq.destination or '-'}",
        f"Message:      {inq.message or '-'}",
    ])
    send_mail(
        subject=f"New contact enquiry — {inq.name}",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.LEADS_NOTIFY_EMAIL],
        fail_silently=True,
    )
    return redirect("core:thank_you")


@require_POST
def callback(request):
    """Callback request — visitor leaves name + phone (+ preferred time) for a call back."""
    d = request.POST
    phone = d.get("phone", "").strip()
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) != 10:
        return JsonResponse({"ok": False, "error": "Phone number must be 10 digits."}, status=400)
    pref = d.get("preferred_time", "").strip()
    inq = Inquiry.objects.create(
        name=d.get("name", "").strip() or "Callback request",
        phone=phone,
        message=f"Preferred time: {pref}" if pref else "",
        source_type=Inquiry.SourceType.CALLBACK,
    )
    send_mail(
        subject=f"New callback request — {inq.name}",
        message=f"Name: {inq.name}\nPhone: {inq.phone}\n{inq.message or ''}".strip(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.LEADS_NOTIFY_EMAIL],
        fail_silently=True,
    )
    return JsonResponse({"ok": True})


@require_POST
def quick_query(request):
    """Lightweight general-query popup — saves a lead and emails the owner (AJAX)."""
    d = request.POST
    inq = Inquiry.objects.create(
        name=d.get("name", "").strip() or "Website visitor",
        phone=d.get("phone", "").strip(),
        message=d.get("message", "").strip(),
        source_type=Inquiry.SourceType.GENERAL,
    )
    send_mail(
        subject=f"New website query — {inq.name}",
        message=f"Name: {inq.name}\nPhone: {inq.phone}\nQuery: {inq.message or '-'}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.LEADS_NOTIFY_EMAIL],
        fail_silently=True,
    )
    return JsonResponse({"ok": True})

