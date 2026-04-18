from collections import OrderedDict

from django.shortcuts import render

from blog.models import Post
from gallery.models import Artwork


def home(request):
    featured = (
        Artwork.objects.select_related("category", "artist")
        .exclude(image_path="")
        .order_by("title")
        .first()
    )
    return render(
        request,
        "pages/home.html",
        {
            "featured": featured,
        },
    )


def about(request):
    return render(request, "pages/about.html")


def gallery_page(request):
    qs = Artwork.objects.select_related("category", "artist").order_by(
        "category__name", "title"
    )
    groups = OrderedDict()
    for artwork in qs:
        label = artwork.category.name if artwork.category else "Uncategorized"
        groups.setdefault(label, []).append(artwork)
    return render(
        request,
        "pages/gallery.html",
        {"category_groups": list(groups.items())},
    )


def inspiration(request):
    posts = Post.objects.select_related("artist").order_by("-post_date", "-id")[:12]
    return render(
        request,
        "pages/inspiration.html",
        {"posts": posts},
    )
