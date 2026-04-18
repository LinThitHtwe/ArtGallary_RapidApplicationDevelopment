from django.db import models

from artists.models import Artist


class Category(models.Model):
    """Category model – ER: CATEGORY (CategoryID PK)."""

    name = models.CharField(max_length=255)

    class Meta:
        db_table = "category"
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Artwork(models.Model):
    """Artwork model – ER: ARTWORK (ArtworkID PK, ArtistID FK, CategoryID FK)."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    image_path = models.CharField(
        max_length=500,
        blank=True,
        default="",
        help_text="Filename under static assets (e.g. FabiolaGambar1.jpg).",
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="artworks",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="artworks",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "artwork"
        ordering = ["title"]

    def __str__(self):
        return self.title
