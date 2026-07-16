# AugyTravel

Django rebuild of **augytravels.com** — a Uttarakhand travel agency (Char Dham Yatra,
Kedarnath, Himalayan tours, transport). Warm, editorial, forest-green + clay design.

Full plan & design system: [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md).
Homepage prototype: [`docs/mockups/homepage-prototype.html`](docs/mockups/homepage-prototype.html).

## Project layout

```
config/            project (settings package, urls, wsgi/asgi)
  settings/        base.py · development.py · production.py  (selected via DJANGO_ENV)
apps/              first-party apps (imported by short name)
  core/            home view, SiteSetting singleton, FAQ, context processor
  destinations/    Destination
  packages/        Package, PackageCategory, ItineraryDay, PackagePoint, PackageImage
  testimonials/    Testimonial
  enquiries/       Enquiry, NewsletterSubscriber
templates/         base.html + partials/ + pages/
static/            css/app.css · js/main.js · img/ (logo SVGs)
media/             uploaded images (gitignored)
docs/              BLUEPRINT.md, mockups/
```

## Run locally (Windows / PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt          # adds Pillow (needed for image fields)
python manage.py migrate
python manage.py createsuperuser          # for the admin
python manage.py runserver
```

Then open:

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/  (edit Site Settings, packages, testimonials, etc.)

Environment defaults to **development**. For production set `DJANGO_ENV=production`
plus the variables in [`.env.example`](.env.example).

## Notes

- `config/settings.py` is superseded by the `config/settings/` package and is now dead
  code — safe to delete.
- Tailwind currently loads via CDN for speed of iteration; a compiled build replaces it
  in Phase 2 (see blueprint).
- Homepage featured packages/destinations/testimonials are placeholder markup for now;
  they get wired to the models once real content is entered (next step in Phase 1).
