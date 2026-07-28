"""
One-time content seeder for the blog.

Usage:
    python manage.py seed_blog

Safe to run more than once: posts/categories are matched by slug and skipped
if they already exist, so it will never overwrite something you edited in the
admin. Cover images are intentionally left blank — upload them in the admin.
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import BlogCategory, BlogPost

CATEGORIES = ["Char Dham", "Kedarnath", "Destinations", "Travel Tips"]

# Each post: (title, slug, category, tags, excerpt, body_html)
POSTS = [
    (
        "Char Dham Yatra 2026: A Complete Beginner's Guide",
        "char-dham-yatra-guide",
        "Char Dham",
        "char dham, yatra, uttarakhand, pilgrimage",
        "Everything a first-timer needs to plan the Char Dham Yatra — the route, best "
        "season, how many days to keep, and what to expect at each dham.",
        """
<p>The Char Dham Yatra covers four sacred shrines in the Garhwal Himalayas —
<strong>Yamunotri, Gangotri, Kedarnath and Badrinath</strong>. For many families it is
a once-in-a-lifetime journey, so a little planning goes a long way.</p>

<h2>The traditional route</h2>
<p>The yatra is done from west to east: Yamunotri first, then Gangotri, Kedarnath and
finally Badrinath. Most travellers start from Haridwar or Dehradun.</p>

<h2>When to go</h2>
<p>The shrines open around late April/early May (Akshaya Tritiya) and close near Diwali.
The most comfortable windows are <strong>May–June</strong> and
<strong>September–October</strong>, avoiding the peak monsoon weeks when landslides are
more likely.</p>

<h2>How many days do you need?</h2>
<ul>
    <li><strong>Full Char Dham by road:</strong> 10–12 days</li>
    <li><strong>Do Dham (Kedarnath + Badrinath):</strong> 6–7 days</li>
    <li><strong>Char Dham with helicopter:</strong> 5–6 days</li>
</ul>

<h2>What to keep ready</h2>
<p>Carry valid photo ID, warm layers even in summer, comfortable walking shoes, and any
regular medication. Mandatory yatra registration is required — we handle this for every
guest so you don't have to.</p>

<blockquote>Our head office sits in the Kedarnath valley itself, so your yatra is
planned by people who travel these roads every season.</blockquote>

<p>Tell us your dates and group size and we'll build a comfortable, women- and
elder-friendly itinerary around them.</p>
""",
    ),
    (
        "Kedarnath Helicopter Booking: Prices, Timings & How It Works",
        "kedarnath-helicopter-booking",
        "Kedarnath",
        "kedarnath, helicopter, heli, booking",
        "A clear, no-jargon guide to the Kedarnath helicopter service — the helipads, "
        "how booking works, and how to plan a smooth same-day darshan.",
        """
<p>Short on time or travelling with elders? The Kedarnath helicopter service turns a
tough 16 km trek into a quick, scenic flight — ideal for a comfortable darshan.</p>

<h2>Where the helicopters fly from</h2>
<p>Services operate from three helipads in the Kedarnath valley —
<strong>Phata, Sersi and Guptkashi</strong>. Each runs shuttle flights up to the
Kedarnath helipad, a short walk from the temple.</p>

<h2>How booking works</h2>
<p>Helicopter tickets are issued through the government's official portal and licensed
operators. Slots in peak season (May–June) sell out very quickly, so early booking is
essential. We coordinate the tickets along with your stay and road transport so the
whole trip is handled in one place.</p>

<h2>Good to know</h2>
<ul>
    <li>Flights depend heavily on weather and may be delayed on cloudy mornings.</li>
    <li>Carry a valid photo ID that matches your booking.</li>
    <li>Baggage is limited — pack light for the flight.</li>
    <li>Round-trip and same-day darshan options are both available.</li>
</ul>

<blockquote>Prices change every season and by operator, so we share live rates when we
plan your dates rather than quoting a number that goes stale.</blockquote>

<p>Send us your preferred travel dates and number of passengers and we'll check
availability for you.</p>
""",
    ),
    (
        "Best Time to Visit Uttarakhand: A Season-by-Season Guide",
        "best-time-to-visit-uttarakhand",
        "Destinations",
        "uttarakhand, seasons, weather, planning",
        "Uttarakhand is beautiful year-round, but each season suits a different kind of "
        "trip. Here's how to pick the right months for yours.",
        """
<p>From snow-dusted peaks to green river valleys, Uttarakhand changes character with
every season. Choosing the right months makes all the difference.</p>

<h2>Spring & Summer (March–June)</h2>
<p>The most popular window. Pleasant days, blooming valleys, and the start of the Char
Dham season. Hill stations like <strong>Mussoorie, Nainital and Auli</strong> are at
their best. Book early — this is peak season.</p>

<h2>Monsoon (July–September)</h2>
<p>Lush and green, with fewer crowds and lower prices, but mountain roads can face
landslides and delays. Better suited to lower-altitude stays than high pilgrimage
routes.</p>

<h2>Autumn (October–November)</h2>
<p>A quiet favourite — clear skies, crisp air and excellent mountain views. Great for
trekking and photography before the winter cold sets in.</p>

<h2>Winter (December–February)</h2>
<p>Snowfall in the higher reaches, perfect for <strong>Auli's skiing</strong> and cosy
hill retreats. The Char Dham shrines are closed, but the winter seats of the deities can
still be visited.</p>

<blockquote>Whatever the season, we match your itinerary to the weather so you spend
your days sightseeing, not stuck on a closed road.</blockquote>
""",
    ),
    (
        "What to Pack for a Himalayan Yatra: The Essentials Checklist",
        "what-to-pack-himalayan-yatra",
        "Travel Tips",
        "packing, checklist, yatra, tips",
        "A practical packing checklist for the Char Dham and other Himalayan trips — "
        "warm layers, documents, and the small things people forget.",
        """
<p>Mountain weather changes fast. Packing right keeps you comfortable and safe through
the yatra — here's what we recommend to every guest.</p>

<h2>Clothing</h2>
<ul>
    <li>Warm layers — even summer mornings are cold at altitude</li>
    <li>A waterproof jacket or poncho</li>
    <li>Comfortable, broken-in walking shoes</li>
    <li>Woollen cap, gloves and warm socks</li>
</ul>

<h2>Documents</h2>
<ul>
    <li>Original photo ID (Aadhaar, passport or voter card)</li>
    <li>Yatra registration — we arrange this for you</li>
    <li>A few passport photos, just in case</li>
</ul>

<h2>Health & comfort</h2>
<ul>
    <li>Personal medicines and a basic first-aid kit</li>
    <li>Sunscreen, lip balm and sunglasses</li>
    <li>A refillable water bottle and some dry snacks</li>
    <li>A power bank — charging points are limited on the route</li>
</ul>

<blockquote>Pack light but smart. On helicopter legs especially, baggage limits are
strict, so a single compact bag works best.</blockquote>

<p>Have questions about a specific route? Just ask — our local team is happy to help you
prepare.</p>
""",
    ),
    (
        "Why Travel With a Local Uttarakhand Agency",
        "why-travel-with-a-local-agency",
        "Travel Tips",
        "local, trust, transparent pricing, about",
        "Booking your Himalayan trip with a local, Uttarakhand-based team means honest "
        "pricing, real ground support, and plans that actually work in the mountains.",
        """
<p>The Himalayas reward good planning and punish guesswork. Travelling with a team based
in Uttarakhand — not a call centre far away — changes the whole experience.</p>

<h2>People who know the roads</h2>
<p>Our head office is in the Kedarnath valley, with branches in Delhi and Dehradun. We
travel these routes every season, so we know which roads clear first after rain, which
stays are genuinely comfortable, and how to plan around the weather.</p>

<h2>Transparent, honest pricing</h2>
<p>No hidden add-ons and no inflated peak-season quotes. You see what you pay for —
stay, transport, permits and darshan — laid out clearly before you commit.</p>

<h2>Comfortable and women-friendly</h2>
<p>We plan trips that families and solo women travellers feel safe on: vetted drivers,
sensible daily distances, and stays we would send our own relatives to.</p>

<h2>Real support on the ground</h2>
<p>If a road closes or a flight is delayed, a local team can actually help. That
on-ground presence is the difference between a stressful day and a smooth one.</p>

<blockquote>Share your dates and what you have in mind — we'll turn it into a plan that
works in the real mountains, not just on paper.</blockquote>
""",
    ),
]


class Command(BaseCommand):
    help = "Seed the blog with starter posts and categories (idempotent)."

    def handle(self, *args, **options):
        User = get_user_model()
        author = User.objects.filter(is_superuser=True).order_by("id").first()
        if author is None:
            self.stdout.write(
                self.style.WARNING(
                    "No superuser found — posts will be created without an author. "
                    "Create one with `python manage.py createsuperuser` and re-run "
                    "to attach an author, or set it in the admin."
                )
            )

        # Categories
        cats = {}
        for name in CATEGORIES:
            cat, created = BlogCategory.objects.get_or_create(name=name)
            cats[name] = cat
            self.stdout.write(("  + " if created else "  = ") + f"category: {name}")

        # Posts — spaced a few days apart so ordering looks natural
        now = timezone.now()
        created_count = 0
        for i, (title, slug, cat_name, tags, excerpt, body) in enumerate(POSTS):
            if BlogPost.objects.filter(slug=slug).exists():
                self.stdout.write(f"  = post exists, skipping: {slug}")
                continue
            BlogPost.objects.create(
                title=title,
                slug=slug,
                author=author,
                category=cats.get(cat_name),
                tags=tags,
                excerpt=excerpt.strip(),
                body=body.strip(),
                published=True,
                published_at=now - timedelta(days=i * 3),
                meta_description=excerpt.strip()[:157],
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"  + post: {slug}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. {created_count} new post(s) created. "
                "Add cover images in the admin, then hard-refresh /blog/."
            )
        )
