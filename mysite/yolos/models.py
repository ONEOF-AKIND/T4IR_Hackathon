from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.
class Search(models.Model):
    # image = models.ImageField(blank=True)
    image = ProcessedImageField(
        # source='image',
        processors=[Thumbnail(500,500)],
        format='JPEG',
        options={'quality':90}
    )