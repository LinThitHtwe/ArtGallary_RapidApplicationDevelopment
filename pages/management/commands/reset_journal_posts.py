"""
Replace every Inspiration / blog post with a fresh set of journal entries.

Usage (from project root):
    python manage.py reset_journal_posts

Requires applied migrations through blog.0004 (no artist column on Post).
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from blog.models import Post


# Titles and bodies read like a working studio journal — no placeholder wording.
_JOURNAL_ROWS = [
    (
        "When the thumbnail lies",
        "Thumbnails that read perfectly at two inches often collapse at full size. "
        "I have started forcing one mid-stage zoom check before committing to edges—"
        "especially around faces and hands, where the eye forgives nothing.",
    ),
    (
        "Borrowing light from cinema",
        "Film stills are unfair teachers: someone already solved the crop, the colour, "
        "and the silence between figures. I keep a small folder of frames that feel "
        "'too simple to work' and try to steal their restraint, not their subject matter.",
    ),
    (
        "Texture last, always",
        "Early grain and paper overlays feel productive; they rarely are. "
        "I leave surfaces clean until values sit where they belong, then add noise "
        "in a single pass so it reads as material, not camouflage.",
    ),
    (
        "Poster logic versus painting logic",
        "Posters want a headline shape—one silhouette the bus rider gets in half a second. "
        "Illustration wants a wandering path. Swapping modes mid-file is how I ruin both; "
        "labeling the layer stack with the mode name keeps me honest.",
    ),
    (
        "Colour scripts for cloudy weeks",
        "Grey afternoons push everything toward mauve mud. I keep three limited palettes "
        "saved as swatches: warm neutrals, cool neutrals, and one 'unreasonable' accent. "
        "Picking one palette before touching the canvas saves a day of second guessing.",
    ),
    (
        "Shipping imperfect leaves",
        "There is a version of every piece that felt finished three hours before the one "
        "I exported. The gap between those two is usually ego, not quality. "
        "Publishing on a calendar—even a soft one—trains the hand to finish without flinching.",
    ),
]


class Command(BaseCommand):
    help = "Delete all posts and insert a new set of journal entries."

    @transaction.atomic
    def handle(self, *args, **options):
        deleted, _ = Post.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"Removed {deleted} post row(s)."))

        now = timezone.now()
        posts = []
        for i, (title, content) in enumerate(_JOURNAL_ROWS):
            # Stagger dates so the Inspiration page reads like a real archive.
            days_ago = 4 + i * 9 + (i % 3) * 2
            posts.append(
                Post(
                    title=title,
                    content=content,
                    post_date=now - timedelta(days=days_ago, hours=i * 3),
                )
            )
        Post.objects.bulk_create(posts)
        self.stdout.write(
            self.style.SUCCESS(f"Inserted {len(posts)} journal entries.")
        )
