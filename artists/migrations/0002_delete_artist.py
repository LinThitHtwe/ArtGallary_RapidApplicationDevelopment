# Drop artist table after foreign keys are removed from post and artwork.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("artists", "0001_initial"),
        ("blog", "0004_remove_post_artist"),
        ("gallery", "0003_remove_artwork_artist"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Artist",
        ),
    ]
