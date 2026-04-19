from django.db import models
from django.utils import timezone


class Post(models.Model):
    """Post model — assignment: PostID, Title, Content, PostDate."""

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "post"
        ordering = ["-post_date", "-id"]

    def __str__(self):
        return self.title
