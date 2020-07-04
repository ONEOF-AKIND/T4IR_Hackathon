from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
# Create your models here.

class Search(models.Model):
    image = models.ImageField(blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors = [Thumbnail(200,300)],
        format = 'JPEG',
        options = {'quality':90}
    )

class Search2(models.Model):
    image = models.ImageField(blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors = [Thumbnail(200,300)],
        format = 'JPEG',
        options = {'quality':90}
    )

