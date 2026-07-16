# Augy Travels — Build Instructions for AI (Claude Cowork)

> **Source of truth.** This document defines what to build: the tech, apps, pages, URLs,
> models, forms, and rules. Build in the order given in Section 12. When something is
> unclear, ask before assuming — especially around anything involving money.
> If any instruction here conflicts with something told later, ask which one wins before building.

---

## 1. Project summary
Website for **Augy Travels**, a travel agency in Rudraprayag, Uttarakhand, India, selling
**Himalayan pilgrimage trips** (Char Dham, Kedarnath). Full rebuild replacing an old WordPress site.
Purpose: **show travel packages + destinations, and collect customer inquiries.** Staff manage all
content through Django Admin.

## 2. Tech stack (use exactly this)
- Backend: Django (latest stable)
- CMS/admin: Django Admin (built-in) — no Wagtail/WordPress/external CMS
- Styling: Tailwind CSS, mobile-first
- Templates: Django templates (server-rendered); no React/SPA unless later requested
- DB: SQLite for dev; structured to move to PostgreSQL for production
- Images: all **self-hosted** in media storage and optimized; never hotlink external domains

## 3. HARD RULES — what NOT to build
- **No payment gateway** (no Razorpay/Stripe/card/online payment of any kind)
- **No real-time booking / availability engine** (no seat counts, calendar availability, confirmed bookings)
- **No CRM** (store inquiries cleanly so they *could* export later — that's all)
- Every "booking"/"booking request" = **an inquiry form that gets saved and emailed to Augy.** Nothing more.
- If a requirement seems to ask for payments, live availability, or a CRM → stop and ask.

## 4. Django apps
- **core** — homepage, About, Contact, base template, site-wide config, nav, footer
- **destinations** — destination pages + content
- **tours** — tour packages + package categories
- **blog** — posts, categories, tags
- **testimonials** — reviews with approval workflow
- **leads** — inquiry forms + stored leads

## 5. Pages (10 templates) — all mobile-responsive
1. Home — hero, featured packages, popular destinations, why-choose-us, testimonials, gallery, blog highlights, inquiry CTA, contact, socials
2. Package List — grid + search + filter (category, destination)
3. Package Detail — full details + inquiry/request form
4. Destination List — grid
5. Destination Detail — full info + related packages + FAQs
6. Blog List — all posts, filter by category/tag, search
7. Blog Detail — article + related + social share
8. About Us — editable content + trust elements
9. Contact — form, WhatsApp, call, address, Google Maps link
10. Thank You — confirmation after any form submit

Also: shared **base template** (header/nav + footer) and a **custom 404 page**.

## 6. URL structure (SEO-friendly slugs, not IDs)
```
/                              Home
/about/                        About Us
/contact/                      Contact
/packages/                     Package List
/packages/<slug>/              Package Detail
/packages/category/<slug>/     Packages by category
/destinations/                 Destination List
/destinations/<slug>/          Destination Detail
/blog/                         Blog List
/blog/<slug>/                  Blog Detail
/blog/category/<slug>/         Blog by category
/thank-you/                    Post-form confirmation
/admin/                        Django Admin (staff only)
```
Slugs auto-generated from titles, admin-editable, lowercase-hyphenated.

## 7. Database models
**destinations.Destination** — name, slug, overview (rich text), attractions, travel_guide,
best_time_to_visit, local_activities, cover_image, is_featured, created_at; has many DestinationImage,
many FAQ, many related TourPackage.

**tours.PackageCategory** — name, slug, description.

**tours.TourPackage** — title, slug, category (FK), destinations (M2M), short_description, price,
duration (e.g. "6 Days / 5 Nights"), itinerary (rich text / repeatable day items), inclusions,
exclusions, accommodation_details, transport_details, terms_and_conditions, cover_image, is_featured,
is_seasonal, created_at; has many PackageImage.

**blog.BlogCategory** — name, slug.
**blog.BlogPost** — title, slug, author, category (FK), tags, excerpt, body (rich text), cover_image,
published (bool), published_at, created_at.

**testimonials.Testimonial** — customer_name, location (opt), rating (1–5), text, video_url (opt),
is_approved (bool, default **False**), is_featured, created_at.

**leads.Inquiry** — name, phone, email, message, source_type (general/package/custom-tour/callback/whatsapp),
related_package (FK, nullable), follow_up_status (new/contacted/closed, default new), created_at.

**core.SiteConfig** (single row) — phone, whatsapp_number, email, address, google_maps_link,
facebook_url, instagram_url, youtube_url.
**core.SitePage** (editable static content) — title, slug, body (rich text).

**Shared FAQ** — question, answer, link to parent (destination / package / general).
**Shared galleries** DestinationImage, PackageImage — image, caption, order, FK to parent.

## 8. Django Admin (this IS the CMS)
Register every model. List views with search + useful filters; inline editing for galleries + FAQs on
parents; `prepopulated_fields` for slugs. Testimonial: easy `is_approved` toggle, unapproved never public.
Inquiry: read-mostly with editable `follow_up_status` (the "lead view"). Staff-only admin.

## 9. Forms & lead handling
Forms (save + notify, no payment): General inquiry (Contact), Package-specific inquiry (Package Detail,
pre-fills package), Custom tour request, Callback request (name + phone). Every form: (1) save Inquiry,
(2) email Augy, (3) spam protection + CAPTCHA, (4) redirect to /thank-you/. Plus a WhatsApp button
(`https://wa.me/<number>`), no form.

## 10. Reusable components (Tailwind, mobile-first)
Header w/ responsive nav (hamburger); footer w/ contact + socials + maps (from SiteConfig); package/
destination/blog/testimonial cards; button + form field styles; click-to-call (`tel:`) + WhatsApp links.

## 11. Security, SEO & performance
HTTPS/SSL settings for prod (secure cookies, https redirect); secure admin; CAPTCHA + spam protection on
all public forms; SEO (clean slugs, editable meta title/description per page/package/post, sitemap.xml,
proper headings); performance (optimize + self-host images, lazy-load, minimize page weight).

## 12. Build order
1. Scaffold project + 6 apps + Tailwind + base template
2. Models (Section 7) + migrations
3. Register everything in admin
4. Base template (header/nav/footer) + reusable components
5. Home page (real data)
6. Packages (list, detail, category filter) + package inquiry form
7. Destinations (list, detail) + related packages + FAQs
8. All lead forms + email + thank-you + admin lead view
9. Blog (list, detail, categories, tags, search, social share)
10. Testimonials with approval workflow + featured section
11. About + Contact pages + contact integrations
12. Security, SEO, performance polish; custom 404
13. Prepare for deployment (prod settings, PostgreSQL, static/media)

## 13. Definition of done
All 10 pages built, mobile-responsive, live data from admin; admin fully manages content; all forms save
a lead AND email Augy with CAPTCHA; testimonials require approval; SEO-friendly slugs + sitemap; all images
self-hosted/optimized, no external/demo images, no placeholder content; runs cleanly, deploy-ready with SSL.
