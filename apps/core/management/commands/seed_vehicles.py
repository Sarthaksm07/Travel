"""
One-time seeder for the rental fleet.

Usage:
    python manage.py seed_vehicles

Idempotent: vehicles are matched by name and skipped if they already exist.
Rates are indicative (with driver); edit them anytime in the admin. Photos are
left blank on purpose — upload them in the admin to replace the icon.
"""

from django.core.management.base import BaseCommand

from core.models import Vehicle

# (name, category, seating, rate, best_for, icon, order)
VEHICLES = [
    ("Swift / Aura", "Sedan", "4 seats", 12,
     "Ideal for couples & small families.", "fas fa-car", 1),
    ("Ertiga / Rumion", "MUV", "6–7 seats", 16,
     "Comfortable for families & small groups.", "fas fa-car-side", 2),
    ("Innova / Crysta", "Premium SUV", "6–7 seats", 19,
     "Extra comfort for long Himalayan drives.", "fas fa-car-side", 3),
    ("Tempo Traveller", "Tempo Traveller", "12–26 seats", 26,
     "12–26 seaters for large yatra groups.", "fas fa-bus", 4),
    ("Force Urbania", "Premium Van", "9–15 seats", 32,
     "9–15 seater luxury van for mid-size groups.", "fas fa-van-shuttle", 5),
]


class Command(BaseCommand):
    help = "Seed the chauffeur-driven rental fleet (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for name, category, seating, rate, best_for, icon, order in VEHICLES:
            if Vehicle.objects.filter(name=name).exists():
                self.stdout.write(f"  = exists, skipping: {name}")
                continue
            Vehicle.objects.create(
                name=name, category=category, seating=seating,
                per_km_rate=rate, best_for=best_for, icon=icon,
                is_active=True, order=order,
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"  + vehicle: {name}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created} new vehicle(s) created. "
            "Edit rates or add photos in the admin, then hard-refresh /vehicles/."))
