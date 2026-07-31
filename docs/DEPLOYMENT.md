# Augy Travels — Deployment Checklist

Tasks required to take the site live. Run migrations first, then the rest.

## 1. Core setup (required)
- [ ] Set environment: `DJANGO_ENV=production`
- [ ] Set a real `DJANGO_SECRET_KEY` (never commit it)
- [ ] `DJANGO_DEBUG=False`
- [ ] Set `DJANGO_ALLOWED_HOSTS` to the real domain(s)
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic`
- [ ] Create admin user (`createsuperuser`) if not present
- [ ] (Optional) Run seed commands for starter content:
      `seed_pages`, `seed_vehicles`, `seed_stats`, `seed_packages`,
      `seed_destinations`, `seed_blog`

## 2. Database
- [ ] Decide SQLite vs PostgreSQL (Postgres recommended for production)
- [ ] Configure DB connection via env vars; migrate

## 3. Static / performance — REMOVES THE FIRST-LOAD FLASH (must-do)
> The brief "unstyled flash" on first load comes from loading Tailwind,
> Font Awesome and Google Fonts from CDNs at runtime. Bundling them fixes it.
- [ ] **Compile Tailwind** into a single local CSS file (drop the
      `https://cdn.tailwindcss.com` runtime script + inline config in base.html).
      Replicate the theme colors/fonts from the current inline config.
- [ ] **Self-host fonts** (Fraunces, Plus Jakarta Sans) with `font-display: swap`.
- [ ] **Self-host / subset Font Awesome** to only the icons used.
- [ ] Serve static via WhiteNoise or Nginx, with gzip/brotli + far-future caching.
- [ ] Compress/optimize uploaded images (packages, destinations, gallery).

## 4. Email (lead notifications)
- [ ] Configure real SMTP backend in production (Gmail app password or
      SendGrid/Zoho/Brevo — all have free tiers).
- [ ] Set `DJANGO_DEFAULT_FROM_EMAIL` and `DJANGO_LEADS_NOTIFY_EMAIL`.
- [ ] Send a test enquiry and confirm it arrives at augytravels@gmail.com.

## 5. Domain, HTTPS, security
- [ ] Point augytravels.com DNS to the server/host.
- [ ] Install SSL certificate (HTTPS).
- [ ] Enable secure cookies + HSTS in production settings.

## 6. SEO / analytics
- [ ] Add Google Analytics (and/or Search Console verification).
- [ ] Add `sitemap.xml` and `robots.txt`.
- [ ] Confirm per-page meta titles/descriptions render (already implemented).

## 7. Media hosting
- [ ] Ensure uploaded media (logo, package/destination/gallery images) is
      served correctly and persists (local media dir or object storage).

## 8. Paused / optional features (decide before or after launch)
- [ ] Spam protection on forms (honeypot + time-check recommended; CAPTCHA optional)
- [ ] True auto-WhatsApp lead delivery (WhatsApp Business Cloud API — paid)
- [ ] Video testimonials display (model field exists)

## 9. Handover
- [ ] Admin user manual + short CMS walkthrough for the owner.
