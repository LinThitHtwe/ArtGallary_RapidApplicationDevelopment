from django.db import models

from artists.models import Artist


class Post(models.Model):
    """Post model – ER: POST (PostID PK, ArtistID FK)."""

    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "post"
        ordering = ["-id"]

    def __str__(self):
        return self.title
