# Generated manually — align schema with assignment (Artwork table only)

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0002_artwork_description_image_path"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artwork",
            name="artist",
        ),
    ]
