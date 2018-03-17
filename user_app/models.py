from __future__ import unicode_literals

from django.db import models
from main_app.models import BaseModel
from django.contrib.auth.models import User
from constants import *

# Create your models here.
class CustomUser(BaseModel):

    user = models.ForeignKey(User)
    mobile = models.CharField("Mobile No", max_length = 12)
    dob = models.DateField("Date of Birth")
    city = models.CharField("City", max_length = 30, 
                    blank = True, null = True)
    country = models.CharField("Country", max_length = 30,
                    blank = True, null = True)
    gender = models.CharField("Gender", max_length = 10,
                    choices = GENDER_CHOICES, default = ' ')

    def __unicode__(self):
        return "%s | %s" %(self.user.get_full_name(), self.user.username)