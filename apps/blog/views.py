from django.shortcuts import render

from .models import BlogCategory, BlogPost


def post_list(request):
    posts = BlogPost.objects.filter(published=True)
    categories = BlogCategory.objects.filter(posts__published=True).distinct()
    return render(request, "pages/blog.html", {"posts": posts, "categories": categories})


def post_detail(request, slug):
    # Non-strict: fall back to the static sample if the post isn't in the DB yet.
    post = BlogPost.objects.filter(slug=slug, published=True).first()
    related = None
    if post:
        qs = BlogPost.objects.filter(published=True).exclude(pk=post.pk)
        if post.category_id:
            qs = qs.filter(category=post.category)
        related = qs[:3]
    return render(request, "pages/blog-detail.html", {"post": post, "related": related})
