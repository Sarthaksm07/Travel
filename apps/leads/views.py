from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from destinations.models import Destination

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
            source_type=(
                Inquiry.SourceType.RENTAL if is_rental
                else Inquiry.SourceType.BOOKING
            ),
        )
        label = "rental enquiry" if is_rental else "trip request"
        body = "\n".join([
            f"New {label} from {inq.name}",
            "",
            f"Phone:        {inq.phone}",
            f"Email:        {inq.email or '-'}",
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
    return render(request, "pages/booking.html", {
        "prefill_vehicle": g.get("vehicle", "").strip(),
        "is_rental": g.get("source", "").strip() == "rental",
        "prefill_destination": g.get("destination", "").strip(),
        "prefill_travel_date": g.get("travel_date", "").strip(),
        "prefill_travellers": g.get("num_travellers", "").strip(),
        "dest_names": list(Destination.objects.values_list("name", flat=True)),
    })


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

