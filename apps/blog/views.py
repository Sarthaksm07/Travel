from django.shortcuts import get_object_or_404, render

from .models import BlogCategory, BlogPost


def post_list(request):
    posts = BlogPost.objects.filter(published=True)
    categories = BlogCategory.objects.filter(posts__published=True).distinct()
    return render(request, "pages/blog.html", {"posts": posts, "categories": categories})


def post_detail(request, slug):
    # Strict: an unknown/renamed slug returns a proper 404 instead of a sample.
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    qs = BlogPost.objects.filter(published=True).exclude(pk=post.pk)
    if post.category_id:
        qs = qs.filter(category=post.category)
    related = qs[:3]
    return render(request, "pages/blog-detail.html", {"post": post, "related": related})
