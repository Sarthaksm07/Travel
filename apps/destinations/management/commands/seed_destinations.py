"""
One-time content seeder for destinations.

Usage:
    python manage.py seed_destinations

Idempotent: destinations are matched by slug and skipped if they already exist,
so re-running never overwrites edits made in the admin. It also links each
destination to relevant packages (if those packages exist) and adds a couple of
FAQs. Cover images are left blank on purpose — upload them in the admin.
"""

from django.core.management.base import BaseCommand

from core.models import FAQ
from destinations.models import Destination
from tours.models import TourPackage


def dest(name, slug, best_time, overview, attractions, guide, activities,
         packages, faqs, featured=False, order=0):
    return dict(
        name=name, slug=slug, best_time=best_time, overview=overview,
        attractions=attractions, guide=guide, activities=activities,
        packages=packages, faqs=faqs, featured=featured, order=order,
    )


DESTINATIONS = [
    dest(
        "Kedarnath", "kedarnath", "May – October",
        "<p>Set against the majestic Kedarnath range at 3,583 m, the Kedarnath temple "
        "is one of the twelve Jyotirlingas and among the holiest of the Char Dham. The "
        "journey — through pine forests, along the Mandakini river, and up a scenic "
        "Himalayan trail — is as moving as the darshan itself.</p>",
        "<ul><li>Kedarnath Jyotirlinga temple</li><li>Bhairavnath temple viewpoint</li>"
        "<li>Vasuki Tal and Gandhi Sarovar</li><li>Adi Shankaracharya Samadhi</li></ul>",
        "<p>Kedarnath is reached by a 16 km trek from Gaurikund, by pony or palki, or by "
        "helicopter from Phata, Sersi or Guptkashi. Our head office is in this very "
        "valley, so we plan the darshan around weather and crowd timings for a smooth trip.</p>",
        "<ul><li>Morning and evening aarti at the temple</li><li>Short treks to Vasuki Tal</li>"
        "<li>Helicopter darshan for elders and families</li></ul>",
        ["kedarnath-yatra", "do-dham-yatra", "char-dham-yatra"],
        [("How do I reach Kedarnath?", "By a 16 km trek from Gaurikund, or by pony, palki or helicopter."),
         ("Is it suitable for elders?", "Yes — with the helicopter option and a well-paced plan, elders travel comfortably.")],
        featured=True, order=1,
    ),
    dest(
        "Badrinath", "badrinath", "May – October",
        "<p>Badrinath, dedicated to Lord Vishnu, sits at 3,133 m between the Nar and "
        "Narayan peaks on the banks of the Alaknanda. One of the four Char Dham shrines, "
        "it is framed by the towering Neelkanth peak and the warm Tapt Kund springs.</p>",
        "<ul><li>Badrinath temple and Tapt Kund</li><li>Mana, India's last village</li>"
        "<li>Vasudhara Falls</li><li>Neelkanth peak views</li></ul>",
        "<p>Badrinath is well connected by road via Joshimath and is the most accessible "
        "of the Char Dham. It pairs naturally with Kedarnath on a Do Dham or full Char "
        "Dham circuit.</p>",
        "<ul><li>Darshan and evening aarti</li><li>Walk to Mana village and Vyas Gufa</li>"
        "<li>Day trip to Vasudhara Falls</li></ul>",
        ["do-dham-yatra", "char-dham-yatra"],
        [("Is Badrinath easy to reach?", "Yes, it is the most road-accessible of the four dhams, via Joshimath.")],
        featured=True, order=2,
    ),
    dest(
        "Rishikesh", "rishikesh", "September – June",
        "<p>Where the Ganga leaves the mountains for the plains, Rishikesh is the world's "
        "yoga capital and the gateway to the Char Dham. Ashrams, riverside cafes, iconic "
        "suspension bridges and white-water rapids sit side by side.</p>",
        "<ul><li>Triveni Ghat Ganga aarti</li><li>Laxman Jhula and Ram Jhula</li>"
        "<li>Beatles Ashram</li><li>White-water rafting stretches</li></ul>",
        "<p>Rishikesh is a short drive from Haridwar and Dehradun, making it an easy "
        "start or end point for a Himalayan trip. It is well suited to families, solo "
        "women travellers and adventure seekers alike.</p>",
        "<ul><li>White-water rafting on the Ganga</li><li>Riverside camping and bonfires</li>"
        "<li>Yoga and meditation retreats</li><li>Evening Ganga aarti</li></ul>",
        ["rishikesh-rafting-camping"],
        [("Is rafting safe for beginners?", "Yes — trained guides, life jackets and graded rapids make it safe for first-timers.")],
        order=3,
    ),
    dest(
        "Haridwar", "haridwar", "September – April",
        "<p>Haridwar, 'the gateway to the gods', is one of the seven holiest cities in "
        "India and where the Ganga first meets the plains. The evening Ganga aarti at "
        "Har Ki Pauri is among the most memorable sights in the country.</p>",
        "<ul><li>Har Ki Pauri and Ganga aarti</li><li>Mansa Devi temple (ropeway)</li>"
        "<li>Chandi Devi temple</li><li>Bustling bazaars</li></ul>",
        "<p>Haridwar has its own railway station and is the usual starting point for the "
        "Char Dham Yatra, well connected to Delhi and Dehradun.</p>",
        "<ul><li>Attend the evening Ganga aarti</li><li>Ropeway to Mansa Devi</li>"
        "<li>Explore the temples and ghats</li></ul>",
        ["char-dham-yatra"],
        [("Is Haridwar the starting point for Char Dham?", "Yes, most yatra itineraries begin and end at Haridwar.")],
        order=4,
    ),
    dest(
        "Auli", "auli", "November – March (snow), April – June (meadows)",
        "<p>Perched above Joshimath at around 2,800 m, Auli is India's premier ski "
        "destination, with velvet meadows in summer and powder snow in winter. Its "
        "cable car offers sweeping views of Nanda Devi, the country's second-highest peak.</p>",
        "<ul><li>Auli ski slopes</li><li>Asia's longest cable car ride</li>"
        "<li>Gurson Bugyal meadows</li><li>Nanda Devi and Trishul views</li></ul>",
        "<p>Auli is reached via a long, scenic drive to Joshimath, then a cable car or "
        "ropeway. Winter is for skiing; spring and summer for meadow walks and views.</p>",
        "<ul><li>Skiing and snowboarding in winter</li><li>Cable car and chairlift rides</li>"
        "<li>Short treks to alpine meadows</li></ul>",
        ["auli-chopta-retreat"],
        [("When can I ski in Auli?", "The ski season typically runs from late December to March, snowfall permitting.")],
        featured=True, order=5,
    ),
    dest(
        "Chopta", "chopta", "March – June, September – November",
        "<p>Often called the 'mini Switzerland of Uttarakhand', Chopta is a serene "
        "meadow hamlet and the base for the Tungnath and Chandrashila treks. Quiet, "
        "green and uncrowded, it is a favourite for nature lovers.</p>",
        "<ul><li>Tungnath, the world's highest Shiva temple</li><li>Chandrashila summit "
        "sunrise</li><li>Deoria Tal lake</li><li>Rolling alpine meadows</li></ul>",
        "<p>Chopta is a scenic drive from Rishikesh or Rudraprayag. The Tungnath trek is "
        "a moderate 3.5 km climb, with the optional Chandrashila summit above it.</p>",
        "<ul><li>Trek to Tungnath and Chandrashila</li><li>Camp near Deoria Tal</li>"
        "<li>Birdwatching and forest walks</li></ul>",
        ["auli-chopta-retreat"],
        [("How hard is the Tungnath trek?", "It is a moderate, well-paved 3.5 km climb suitable for most fitness levels.")],
        order=6,
    ),
    dest(
        "Nainital", "nainital", "March – June, September – November",
        "<p>Built around the emerald Naini Lake in the Kumaon hills, Nainital is a "
        "classic colonial-era hill station. Boat rides, ropeways and viewpoints make it "
        "a relaxed getaway for couples and families.</p>",
        "<ul><li>Naini Lake boating</li><li>Naina Devi temple</li>"
        "<li>Snow View Point (ropeway)</li><li>The Mall Road and Tiffin Top</li></ul>",
        "<p>Nainital is reached by road from Kathgodam, the nearest railhead. It pairs "
        "well with a wildlife add-on at nearby Jim Corbett.</p>",
        "<ul><li>Boat rides on Naini Lake</li><li>Ropeway to Snow View Point</li>"
        "<li>Strolls along the Mall Road</li></ul>",
        ["nainital-getaway"],
        [("Is Nainital good for a honeymoon?", "Yes — lake views, cosy stays and gentle sightseeing make it ideal for couples.")],
        order=7,
    ),
    dest(
        "Jim Corbett", "jim-corbett", "November – June",
        "<p>India's oldest national park, Jim Corbett is a haven of sal forests, "
        "grasslands and the Ramganga river — home to Bengal tigers, elephants, deer and "
        "over 600 bird species. A jeep safari here is a highlight of any Uttarakhand trip.</p>",
        "<ul><li>Jeep safaris across core and buffer zones</li><li>Bengal tiger sightings</li>"
        "<li>Rich birdlife along the Ramganga</li><li>Dhikala grasslands</li></ul>",
        "<p>Corbett is an easy drive from Ramnagar, the nearest railhead. Safari permits "
        "are limited and zone-based, so we book them in advance for you.</p>",
        "<ul><li>Morning and evening jeep safaris</li><li>Birdwatching and nature walks</li>"
        "<li>Riverside stays near the park</li></ul>",
        ["jim-corbett-safari"],
        [("Are tiger sightings guaranteed?", "No safari can guarantee sightings, but Corbett has one of India's highest tiger densities.")],
        order=8,
    ),
    dest(
        "Valley of Flowers", "valley-of-flowers", "July – early September",
        "<p>A UNESCO World Heritage Site, the Valley of Flowers bursts into a carpet of "
        "alpine blooms each monsoon. This high-altitude national park, reached on foot, "
        "is one of the most beautiful treks in the Himalayas.</p>",
        "<ul><li>Hundreds of alpine flower species</li><li>Pushpawati river and glaciers</li>"
        "<li>Nearby Hemkund Sahib</li><li>Snow-fed mountain views</li></ul>",
        "<p>The valley opens only in the monsoon, when the flowers bloom. It is a trek "
        "from Ghangaria, itself reached on foot from Govindghat via Joshimath.</p>",
        "<ul><li>Guided trek into the blooming valley</li><li>Pilgrimage to Hemkund Sahib</li>"
        "<li>Alpine photography</li></ul>",
        ["valley-of-flowers-trek"],
        [("When do the flowers bloom?", "Peak bloom is mid-July to mid-August, during the monsoon window.")],
        order=9,
    ),
]


class Command(BaseCommand):
    help = "Seed destinations, link relevant packages, and add FAQs (idempotent)."

    def handle(self, *args, **options):
        created_count = 0
        for d in DESTINATIONS:
            if Destination.objects.filter(slug=d["slug"]).exists():
                self.stdout.write(f"  = destination exists, skipping: {d['slug']}")
                continue
            obj = Destination.objects.create(
                name=d["name"],
                slug=d["slug"],
                best_time_to_visit=d["best_time"],
                overview=d["overview"],
                attractions=d["attractions"],
                travel_guide=d["guide"],
                local_activities=d["activities"],
                is_featured=d["featured"],
                order=d["order"],
                meta_description=(d["overview"]
                                  .replace("<p>", "").replace("</p>", "")[:157]),
            )
            # Link packages that exist
            pkgs = TourPackage.objects.filter(slug__in=d["packages"])
            if pkgs:
                obj.packages.set(pkgs)
            # FAQs
            for i, (q, a) in enumerate(d["faqs"]):
                FAQ.objects.get_or_create(
                    destination=obj, question=q,
                    defaults={"answer": a, "order": i},
                )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(
                f"  + destination: {d['slug']} ({pkgs.count()} package link(s))"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created_count} new destination(s) created. "
            "Add cover images in the admin, then hard-refresh /destinations/."))
