# Generated manually for art gallery assignment

from django.db import migrations, models


def seed_gallery(apps, schema_editor):
    Artist = apps.get_model("artists", "Artist")
    Category = apps.get_model("gallery", "Category")
    Artwork = apps.get_model("gallery", "Artwork")

    artist, _ = Artist.objects.get_or_create(name="Studio Radiance")

    cat_map = {}
    for name in ("Digital illustrations", "Posters", "Concept art"):
        c, _ = Category.objects.get_or_create(name=name)
        cat_map[name] = c

    rows = [
        (
            "Neon Bloom",
            "A vapor-inspired portrait study in soft pinks and symbols.",
            "FabiolaGambar1.jpg",
            "Digital illustrations",
        ),
        (
            "Urban Echo",
            "Psychedelic rhythm through color, pattern, and proportion.",
            "ValentinGambar.jpg",
            "Posters",
        ),
        (
            "Noir Suitcase",
            "Surreal narrative moment with high contrast and mood.",
            "BillyGambar.jpg",
            "Concept art",
        ),
        (
            "Silver Lines",
            "Architectural mood in cool monochrome and light.",
            "DavidGambar1.jpg",
            "Digital illustrations",
        ),
        (
            "Spectrum Shift",
            "Pop-culture energy with clean gradients and form.",
            "KyleGambar.jpg",
            "Posters",
        ),
    ]

    for title, description, image_path, cat_name in rows:
        Artwork.objects.get_or_create(
            title=title,
            defaults={
                "description": description,
                "image_path": image_path,
                "artist": artist,
                "category": cat_map[cat_name],
            },
        )


def unseed_gallery(apps, schema_editor):
    Artwork = apps.get_model("gallery", "Artwork")
    Category = apps.get_model("gallery", "Category")
    Artist = apps.get_model("artists", "Artist")
    titles = [
        "Neon Bloom",
        "Urban Echo",
        "Noir Suitcase",
        "Silver Lines",
        "Spectrum Shift",
    ]
    Artwork.objects.filter(title__in=titles).delete()
    Category.objects.filter(
        name__in=("Digital illustrations", "Posters", "Concept art")
    ).delete()
    Artist.objects.filter(name="Studio Radiance").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="artwork",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="artwork",
            name="image_path",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Filename under static assets (e.g. FabiolaGambar1.jpg).",
                max_length=500,
            ),
        ),
        migrations.RunPython(seed_gallery, unseed_gallery),
    ]
