"""
One-time seeder for the homepage trust-strip stats.

Usage:
    python manage.py seed_stats

Idempotent: stats are matched by label and skipped if they already exist.
Edit the values anytime in the admin (Core > Stats).
"""

from django.core.management.base import BaseCommand

from core.models import Stat

STATS = [
    ("6000+", "Happy Travellers", "fas fa-users", 1),
    ("4.8", "Google Rating", "fas fa-star", 2),
    ("50+", "Tour Packages", "fas fa-mountain-sun", 3),
    ("100%", "Women-Friendly", "fas fa-shield-heart", 4),
]


class Command(BaseCommand):
    help = "Seed homepage trust-strip stats (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for value, label, icon, order in STATS:
            if Stat.objects.filter(label=label).exists():
                self.stdout.write(f"  = exists, skipping: {label}")
                continue
            Stat.objects.create(value=value, label=label, icon=icon, order=order, is_active=True)
            created += 1
            self.stdout.write(self.style.SUCCESS(f"  + stat: {label}"))
        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created} new stat(s). Edit values in the admin (Core > Stats)."))
