"""
One-time content seeder for tour packages.

Usage:
    python manage.py seed_packages

Idempotent: categories and packages are matched by slug and skipped if they
already exist, so re-running never overwrites edits you make in the admin.
Cover images are left blank on purpose — upload them in the admin.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from tours.models import PackageCategory, TourPackage

# (name, slug, order)
CATEGORIES = [
    ("Uttarakhand", "uttarakhand", 1),
    ("Adventure", "adventure", 2),
    ("Wildlife & Safari", "wildlife", 3),
    ("Honeymoon", "honeymoon", 4),
]

INC = """<ul>
<li>Accommodation on twin-sharing basis in hand-picked hotels</li>
<li>Daily breakfast and dinner</li>
<li>All sightseeing and transfers by private vehicle</li>
<li>Experienced, hill-trained driver</li>
<li>Toll, parking, state taxes and driver allowance</li>
<li>All applicable GST</li>
</ul>"""

EXC = """<ul>
<li>Train or air fare to the starting point</li>
<li>Lunch and personal expenses</li>
<li>Helicopter tickets, pony or palki charges (where applicable)</li>
<li>Entry fees, guide charges and adventure-activity costs unless specified</li>
<li>Anything not listed under inclusions</li>
</ul>"""

TERMS = """<ul>
<li>Prices are indicative and confirmed at the time of booking based on your dates and group size.</li>
<li>A booking advance confirms your reservation; the balance is payable before travel.</li>
<li>Itineraries may adjust for weather, road conditions or darshan timings — your safety comes first.</li>
<li>Cancellation terms are shared in writing before you confirm.</li>
</ul>"""


def package(title, slug, cat, price, duration, short, itinerary,
            accommodation, transport, featured=False, order=0):
    return dict(
        title=title, slug=slug, cat=cat, price=price, duration=duration,
        short=short, itinerary=itinerary, accommodation=accommodation,
        transport=transport, featured=featured, order=order,
    )


PACKAGES = [
    package(
        "Char Dham Yatra", "char-dham-yatra", "uttarakhand", None, "10 Days / 9 Nights",
        "The complete Himalayan pilgrimage to Yamunotri, Gangotri, Kedarnath and "
        "Badrinath — planned end to end by a local team that travels these valleys "
        "every season. Comfortable, unhurried and genuinely women- and elder-friendly.",
        """<p>A relaxed ten-day circuit through the four sacred dhams of Garhwal, paced so
elders and families travel comfortably.</p>
<h3>Day 1 — Haridwar to Barkot</h3><p>Arrival, meet your guide and a scenic drive to Barkot for an overnight stay.</p>
<h3>Day 2 — Yamunotri Darshan</h3><p>Trek or pony to the Yamunotri temple, darshan, and return to Barkot.</p>
<h3>Day 3 — Barkot to Uttarkashi</h3><p>Drive along the Bhagirathi to Uttarkashi; evening at leisure.</p>
<h3>Day 4 — Gangotri Darshan</h3><p>Visit Gangotri, the source of the Ganga, then back to Uttarkashi.</p>
<h3>Days 5–7 — Kedarnath</h3><p>Drive to Guptkashi, then trek or take the helicopter to Kedarnath for darshan and stay.</p>
<h3>Days 8–9 — Badrinath</h3><p>Journey to Badrinath, darshan and a visit to Mana, India's last village, then to Rudraprayag.</p>
<h3>Day 10 — Return to Haridwar</h3><p>A scenic drive back to Haridwar where the trip concludes.</p>""",
        "<p>Clean, comfortable hotels and guesthouses hand-picked for each stop, on a "
        "twin-sharing basis. At Kedarnath, simple mountain lodging close to the temple.</p>",
        "<p>A private, well-maintained vehicle throughout with an experienced hill "
        "driver. Vehicle size is matched to your group — from a sedan to a Tempo Traveller.</p>",
        featured=True, order=1,
    ),
    package(
        "Do Dham Yatra (Kedarnath & Badrinath)", "do-dham-yatra", "uttarakhand", 12999,
        "6 Days / 5 Nights",
        "The two most-visited dhams — Kedarnath and Badrinath — in a compact, "
        "well-paced week. Ideal if you're short on time but don't want to miss the "
        "heart of the Char Dham.",
        """<h3>Day 1 — Haridwar to Guptkashi</h3><p>Drive through Devprayag and Rudraprayag to Guptkashi for the night.</p>
<h3>Day 2 — Kedarnath</h3><p>Trek or helicopter to Kedarnath; darshan and overnight near the temple.</p>
<h3>Day 3 — Return to Guptkashi</h3><p>Morning darshan, then descend and drive to your next stay.</p>
<h3>Day 4 — Badrinath</h3><p>Drive to Badrinath via Joshimath; evening aarti.</p>
<h3>Day 5 — Badrinath & Mana</h3><p>Darshan, visit Mana village, then drive to Rudraprayag.</p>
<h3>Day 6 — Return to Haridwar</h3><p>Scenic drive back; trip concludes.</p>""",
        "<p>Comfortable twin-sharing hotels at each halt, with simple, clean lodging at Kedarnath.</p>",
        "<p>Private vehicle with a hill-experienced driver for the full circuit.</p>",
        featured=True, order=2,
    ),
    package(
        "Kedarnath Yatra", "kedarnath-yatra", "uttarakhand", 10999, "4 Days / 3 Nights",
        "A focused trip to Kedarnath for those who want darshan without a long "
        "itinerary. Trek or fly in by helicopter — we handle the logistics either way.",
        """<h3>Day 1 — Haridwar to Guptkashi</h3><p>Scenic drive along the Mandakini; overnight at Guptkashi.</p>
<h3>Day 2 — Kedarnath</h3><p>Trek from Gaurikund or take the helicopter; darshan and overnight.</p>
<h3>Day 3 — Return to Guptkashi</h3><p>Morning darshan, descend and rest.</p>
<h3>Day 4 — Return to Haridwar</h3><p>Drive back to Haridwar; trip concludes.</p>""",
        "<p>Clean hotels at Guptkashi and simple lodging near the Kedarnath temple.</p>",
        "<p>Private vehicle up to Sonprak/Gaurikund; helicopter coordination on request.</p>",
        order=3,
    ),
    package(
        "Auli & Chopta Snow Retreat", "auli-chopta-retreat", "uttarakhand", 9999,
        "5 Days / 4 Nights",
        "Meadows, snow and some of Garhwal's finest mountain views — a calm getaway "
        "through Auli, Chopta and Tungnath, away from the pilgrimage rush.",
        """<h3>Day 1 — Haridwar to Joshimath</h3><p>Long, scenic drive along the Alaknanda; overnight at Joshimath.</p>
<h3>Day 2 — Auli</h3><p>Cable car to Auli, time in the meadows and views of Nanda Devi.</p>
<h3>Day 3 — Joshimath to Chopta</h3><p>Drive to Chopta, the "mini Switzerland" of Uttarakhand.</p>
<h3>Day 4 — Tungnath & Chandrashila</h3><p>Trek to Tungnath temple and, if fit, Chandrashila summit for sunrise views.</p>
<h3>Day 5 — Return to Haridwar</h3><p>Drive back; trip concludes.</p>""",
        "<p>Comfortable hotels and cosy mountain stays at Joshimath and Chopta.</p>",
        "<p>Private vehicle throughout with a driver who knows the high roads well.</p>",
        order=4,
    ),
    package(
        "Rishikesh Rafting & Camping", "rishikesh-rafting-camping", "adventure", 4999,
        "2 Days / 1 Night",
        "White-water rafting on the Ganga plus a riverside camp night — a quick, "
        "high-energy escape that's perfect for friends and families.",
        """<h3>Day 1 — Rafting & Camp</h3><p>Arrive at Rishikesh, gear up and raft the Ganga's rapids, then check into a riverside camp with a bonfire evening.</p>
<h3>Day 2 — Activities & Departure</h3><p>Morning activities — a short trek or cliff jump — breakfast and departure.</p>""",
        "<p>Riverside Swiss-tent camp on twin/triple sharing, with common washrooms.</p>",
        "<p>Transfers to and from the rafting point; private vehicle on request.</p>",
        order=5,
    ),
    package(
        "Valley of Flowers Trek", "valley-of-flowers-trek", "adventure", 13999,
        "6 Days / 5 Nights",
        "A guided monsoon trek into the UNESCO World Heritage Valley of Flowers, "
        "combined with a visit to the sacred Hemkund Sahib.",
        """<h3>Day 1 — Haridwar to Joshimath</h3><p>Drive along the Alaknanda; overnight at Joshimath.</p>
<h3>Day 2 — Govindghat to Ghangaria</h3><p>Drive to Govindghat and trek up to Ghangaria, the base village.</p>
<h3>Day 3 — Valley of Flowers</h3><p>Full-day trek into the blooming valley; return to Ghangaria.</p>
<h3>Day 4 — Hemkund Sahib</h3><p>Steep climb to the glacial Hemkund Sahib lake and gurudwara.</p>
<h3>Day 5 — Ghangaria to Joshimath</h3><p>Trek down and drive back to Joshimath.</p>
<h3>Day 6 — Return to Haridwar</h3><p>Drive back; trip concludes.</p>""",
        "<p>Simple, clean guesthouses at Joshimath and Ghangaria on sharing basis.</p>",
        "<p>Private vehicle to the trek base; the trek itself is on foot with a guide.</p>",
        order=6,
    ),
    package(
        "Jim Corbett Wildlife Safari", "jim-corbett-safari", "wildlife", 4000,
        "2 Days / 1 Night",
        "A jeep safari weekend in India's oldest national park — tigers, elephants and "
        "birdlife along the Ramganga, with a comfortable jungle-side stay.",
        """<h3>Day 1 — Arrival & Evening Safari</h3><p>Check in near the park, then an afternoon jeep safari into a buffer zone.</p>
<h3>Day 2 — Morning Safari & Departure</h3><p>Early-morning core-zone safari, breakfast and departure.</p>""",
        "<p>Comfortable resort or jungle lodge near the park, on twin-sharing basis.</p>",
        "<p>Private transfers plus permitted jeep safaris with a registered guide.</p>",
        order=7,
    ),
    package(
        "Nainital Romantic Getaway", "nainital-getaway", "honeymoon", 14999,
        "3 Days / 2 Nights",
        "A gentle lakeside honeymoon in Nainital and Kumaon — boat rides, viewpoints "
        "and quiet evenings, arranged with couples in mind.",
        """<h3>Day 1 — Arrival & Naini Lake</h3><p>Arrive in Nainital, settle in and enjoy an evening boat ride on Naini Lake.</p>
<h3>Day 2 — Sightseeing</h3><p>Snow View Point, Naina Devi temple and the surrounding lakes; a relaxed couple's day.</p>
<h3>Day 3 — Departure</h3><p>Leisurely morning, last views and departure.</p>""",
        "<p>A romantic lake-view hotel room with thoughtful couple's touches.</p>",
        "<p>Private vehicle for all transfers and sightseeing.</p>",
        order=8,
    ),
]


class Command(BaseCommand):
    help = "Seed tour packages and categories (idempotent)."

    def handle(self, *args, **options):
        cats = {}
        for name, slug, order in CATEGORIES:
            cat, created = PackageCategory.objects.get_or_create(
                slug=slug, defaults={"name": name, "order": order}
            )
            cats[slug] = cat
            self.stdout.write(("  + " if created else "  = ") + f"category: {name}")

        created_count = 0
        for p in PACKAGES:
            if TourPackage.objects.filter(slug=p["slug"]).exists():
                self.stdout.write(f"  = package exists, skipping: {p['slug']}")
                continue
            TourPackage.objects.create(
                title=p["title"],
                slug=p["slug"],
                category=cats.get(p["cat"]),
                short_description=p["short"],
                price=p["price"],
                duration=p["duration"],
                itinerary=p["itinerary"].strip(),
                inclusions=INC,
                exclusions=EXC,
                accommodation_details=p["accommodation"],
                transport_details=p["transport"],
                terms_and_conditions=TERMS,
                is_featured=p["featured"],
                order=p["order"],
                meta_description=p["short"][:157],
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"  + package: {p['slug']}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. {created_count} new package(s) created. "
                "Add cover images in the admin, then hard-refresh /packages/."
            )
        )
