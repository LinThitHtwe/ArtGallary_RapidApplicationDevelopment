from collections import OrderedDict

from django.shortcuts import render

from blog.models import Post
from gallery.models import Artwork, Category


def _collage_three(artworks):
    """Up to three pieces for the fanned collage; repeat if the DB has fewer."""
    if not artworks:
        return []
    out = list(artworks[:3])
    i = 0
    while len(out) < 3:
        out.append(artworks[i % len(artworks)])
        i += 1
    return out[:3]


def home(request):
    strip_qs = (
        Artwork.objects.select_related("category")
        .exclude(image_path="")
        .order_by("title")
    )
    strip_artworks = list(strip_qs[:10])
    featured = strip_artworks[0] if strip_artworks else None
    collage_three = _collage_three(strip_artworks)

    # For the pinned horizontal "Scroll the wall" section we want a longer reel.
    # Repeat the queryset until we have at least ~12 items (looks great even on tiny seed DBs).
    wall_artworks = []
    if strip_artworks:
        i = 0
        while len(wall_artworks) < 12:
            wall_artworks.append(strip_artworks[i % len(strip_artworks)])
            i += 1
    wall_artworks = wall_artworks[:12]

    # For the bento grid, pick a variety of pieces (different from first showcase)
    bento_artworks = []
    if strip_artworks:
        # Reverse + slice to vary order from the wall
        rotated = strip_artworks[::-1]
        i = 0
        while len(bento_artworks) < 7:
            bento_artworks.append(rotated[i % len(rotated)])
            i += 1
    bento_artworks = bento_artworks[:7]

    latest_post = Post.objects.order_by("-post_date", "-id").first()

    category_names = list(Category.objects.values_list("name", flat=True)[:8])
    studio_terms = [
        "Studio Radiance",
        "Colour studies",
        "Late sketches",
        "Quiet compositions",
    ]
    marquee_terms = [n for n in list(category_names) + studio_terms if n]
    if not marquee_terms:
        marquee_terms = ["Posters", "Concept art", "Illustration"]

    stats = {
        "works": Artwork.objects.count(),
        "posts": Post.objects.count(),
        "categories": Category.objects.count(),
    }

    return render(
        request,
        "pages/home.html",
        {
            "featured": featured,
            "strip_artworks": strip_artworks,
            "collage_three": collage_three,
            "wall_artworks": wall_artworks,
            "bento_artworks": bento_artworks,
            "latest_post": latest_post,
            "marquee_terms": marquee_terms,
            "stats": stats,
        },
    )


def about(request):
    return render(request, "pages/about.html")


def gallery_page(request):
    qs = Artwork.objects.select_related("category").order_by("category__name", "title")
    groups = OrderedDict()
    for artwork in qs:
        label = artwork.category.name if artwork.category else "Uncategorized"
        groups.setdefault(label, []).append(artwork)
    preview = list(qs.exclude(image_path="")[:6])
    return render(
        request,
        "pages/gallery.html",
        {
            "category_groups": list(groups.items()),
            "gallery_total_works": qs.count(),
            "gallery_preview": preview,
        },
    )


def inspiration(request):
    posts = Post.objects.order_by("-post_date", "-id")[:12]
    return render(
        request,
        "pages/inspiration.html",
        {"posts": posts},
    )
