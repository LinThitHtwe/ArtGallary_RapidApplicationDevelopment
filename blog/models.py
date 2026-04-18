from django.db import models
from django.utils import timezone

from artists.models import Artist


class Post(models.Model):
    """Post model – ER: POST (PostID PK, ArtistID FK)."""

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    post_date = models.DateTimeField(default=timezone.now)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "post"
        ordering = ["-post_date", "-id"]

    def __str__(self):
        return self.title
