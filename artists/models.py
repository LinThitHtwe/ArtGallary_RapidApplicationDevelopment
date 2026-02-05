from django.db import models


class Artist(models.Model):
    """Artist model – ER: ARTIST (ArtistID PK)."""

    name = models.CharField(max_length=255)

    class Meta:
        db_table = "artist"
        ordering = ["name"]

    def __str__(self):
        return self.name
