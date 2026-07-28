"""
One-time seeder for legal/static pages (Privacy Policy, Terms & Conditions).

Usage:
    python manage.py seed_pages

Idempotent: pages are matched by slug and skipped if they already exist, so
re-running never overwrites edits you make in the admin. The content is a solid
starting draft written for Augy Travels — review it (ideally with a legal
professional) and edit freely in the admin (Core > Site pages).
"""

from django.core.management.base import BaseCommand

from core.models import SitePage

PRIVACY = """
<p>Augy Travels ("we", "us", "our") respects your privacy. This policy explains what
information we collect when you use our website and how we use it.</p>

<h2>Information we collect</h2>
<p>When you submit an enquiry, booking request, callback or contact form, we collect the
details you provide — typically your name, phone number, email address, travel dates,
group size and any message. We may also collect basic, non-identifying usage data (such
as pages visited) to improve the website.</p>

<h2>How we use your information</h2>
<ul>
<li>To respond to your enquiries and prepare travel plans and quotes.</li>
<li>To contact you about your trip by phone, WhatsApp or email.</li>
<li>To improve our services and website experience.</li>
</ul>

<h2>Sharing your information</h2>
<p>We do not sell your personal information. We may share necessary details with trusted
partners (such as hotels, transport operators or guides) solely to fulfil your travel
arrangements.</p>

<h2>Data retention &amp; security</h2>
<p>We keep enquiry details only as long as needed to serve you and for reasonable
record-keeping. We take sensible measures to protect your information, though no method
of transmission over the internet is completely secure.</p>

<h2>Your choices</h2>
<p>You can ask us to update or delete your details at any time by contacting us using the
information on our Contact page.</p>

<h2>Third-party links</h2>
<p>Our site may link to third-party services (such as WhatsApp, Google Maps or social
media). Their use of your data is governed by their own privacy policies.</p>

<h2>Updates to this policy</h2>
<p>We may update this policy from time to time. The latest version will always be
available on this page.</p>
"""

TERMS = """
<p>These terms govern your use of the Augy Travels website and the enquiry and booking
services offered through it. By using this website, you agree to these terms.</p>

<h2>Enquiries &amp; bookings</h2>
<p>Submitting an enquiry or booking request through this website does not constitute a
confirmed booking. All trips are confirmed only after we discuss your requirements,
share a quote, and you accept it in writing. Prices shown are indicative and confirmed at
the time of booking based on your dates, group size and season.</p>

<h2>Payments</h2>
<p>We do not collect payments through this website. Any advance or balance payments are
arranged directly with our team and communicated to you clearly before you confirm.</p>

<h2>Itineraries &amp; changes</h2>
<p>Itineraries may be adjusted due to weather, road conditions, government regulations,
darshan timings or circumstances beyond our control. Your safety is always our first
priority, and we will suggest the best available alternatives.</p>

<h2>Cancellations &amp; refunds</h2>
<p>Cancellation and refund terms depend on the specific package, season and third-party
policies (hotels, helicopter services, etc.). The applicable terms will be shared with you
in writing before you confirm your booking.</p>

<h2>Your responsibilities</h2>
<ul>
<li>Provide accurate information when making an enquiry or booking.</li>
<li>Carry valid identification and any required documents for your journey.</li>
<li>Follow the guidance of our team and local authorities during your trip.</li>
</ul>

<h2>Liability</h2>
<p>We act in good faith to arrange comfortable, safe journeys, but we are not liable for
losses arising from events beyond our reasonable control, including natural events, road
closures or third-party service failures.</p>

<h2>Contact</h2>
<p>For any questions about these terms, please reach us through our Contact page.</p>
"""

PAGES = [
    ("Privacy Policy", "privacy-policy",
     "Augy Travels privacy policy — what we collect and how we use it.", PRIVACY),
    ("Terms & Conditions", "terms-and-conditions",
     "Augy Travels terms & conditions for enquiries and bookings.", TERMS),
]


class Command(BaseCommand):
    help = "Seed Privacy Policy and Terms & Conditions pages (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for title, slug, meta, body in PAGES:
            if SitePage.objects.filter(slug=slug).exists():
                self.stdout.write(f"  = exists, skipping: {slug}")
                continue
            SitePage.objects.create(
                title=title, slug=slug,
                body=body.strip(), meta_description=meta,
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"  + page: {slug}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created} new page(s) created. "
            "Review/edit them in the admin (Core > Site pages)."))
