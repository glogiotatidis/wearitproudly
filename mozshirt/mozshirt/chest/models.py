from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import SmartResize, ResizeToFit, ResizeToFill
from taggit.managers import TaggableManager

class Shirt(models.Model):
    uploaded_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=300, default='Unknown',
                                  blank=True,
                                  help_text='e.g. Mozilla Corp, Greek Community')
    introduced = models.CharField(blank=True, default='Unknown',
                                  max_length=300,
                                  help_text='e.g. MozCamp, 15th Anniversary')
    description = models.TextField(blank=True, default='')
    owned_by = models.ManyToManyField(User, related_name='owns', blank=True)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return unicode(self.id)

    @property
    def image(self):
        return self.shots.all()[0].image

    @property
    def thumbnail(self):
        return self.shots.all()[0].thumbnail

    @property
    def thumbnail_small(self):
        return self.shots.all()[0].thumbnail_small

    class Meta:
        ordering = ['-created_at']

class ShirtShot(models.Model):
    uploaded_by = models.ForeignKey(User, related_name='shots')
    shirt = models.ForeignKey(Shirt, related_name='shots')
    image = ProcessedImageField([ResizeToFit(2500, 2500)],
                                format='JPEG', options={'quality': 98},
                                upload_to=settings.IMAGE_UPLOAD_PATH)
    thumbnail = ImageSpecField([SmartResize(232, 232)], image_field='image',
                               format='JPEG', options={'quality': 95})
    thumbnail_small = ImageSpecField([SmartResize(85, 85)], image_field='image',
                                     format='JPEG', options={'quality': 95})
    cover = models.BooleanField(blank=True, default=False)

    def __unicode__(self):
        return self.image.name

    class Meta:
        ordering = ['cover']
