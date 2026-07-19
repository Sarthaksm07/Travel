from django.shortcuts import render


def post_list(request):
    return render(request, "pages/blog.html")


def post_detail(request, slug):
    # Static for now — one template serves as the sample for every post.
    # When we go dynamic:
    #   post = get_object_or_404(BlogPost, slug=slug, published=True)
    #   return render(request, "pages/blog-detail.html", {"post": post})
    return render(request, "pages/blog-detail.html")
