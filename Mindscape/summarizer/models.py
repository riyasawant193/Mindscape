from django.db import models

class YouTubeVideo(models.Model):
    url = models.URLField()
    summarized_text = models.TextField(blank=True, null=True)
