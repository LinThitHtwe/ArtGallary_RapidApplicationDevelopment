# Generated manually for art gallery assignment

import datetime

from django.db import migrations, models
from django.utils import timezone


def seed_posts(apps, schema_editor):
    Artist = apps.get_model("artists", "Artist")
    Post = apps.get_model("blog", "Post")

    artist, _ = Artist.objects.get_or_create(name="Studio Radiance")

    rows = [
        (
            "Sketching light before color",
            "Start every piece as a question of light, not pigment. "
            "Blocking shapes early keeps the composition honest.",
            timezone.now() - datetime.timedelta(days=5),
        ),
        (
            "Finding rhythm in repetition",
            "Small daily studies add up: ten minutes of linework trains "
            "the hand more than one long marathon session.",
            timezone.now() - datetime.timedelta(days=12),
        ),
        (
            "Borrowing from film stills",
            "Cropping like a cinematographer gives posters instant drama—"
            "try extreme negative space around a single focal object.",
            timezone.now() - datetime.timedelta(days=20),
        ),
    ]

    for title, content, post_date in rows:
        Post.objects.get_or_create(
            title=title,
            defaults={
                "content": content,
                "post_date": post_date,
                "artist": artist,
            },
        )


def unseed_posts(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    titles = [
        "Sketching light before color",
        "Finding rhythm in repetition",
        "Borrowing from film stills",
    ]
    Post.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="content",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="post",
            name="post_date",
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.RunPython(seed_posts, unseed_posts),
    ]
