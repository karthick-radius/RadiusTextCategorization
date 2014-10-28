from django.db import models

# Create your models here.

class Business(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    @property
    def __unicode__(self):
        return self.name