# Generated manually — align schema with assignment (Post table only)

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_post_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="artist",
        ),
    ]
