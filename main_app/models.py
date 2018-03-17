from __future__ import unicode_literals

from django.db import models

# Create your models here.
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    active = models.PositiveIntegerField(default = 2)

    class Meta:
        abstract = True
