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
    bio = models.TextField("User bio", blank = True, null = True)


    def __unicode__(self):
        return "%s | %s" %(self.user.get_full_name(), self.user.username)


    def is_following(self):
        if self.following_user.filter(active = 2).exists():
            return True
        else:
            return False


    def users_following(self):
        if self.is_following():
            flwuobjs = self.following_user.filter(active = 2)
            return [i.followed for i in flwuobjs]
        else:
            return CustomUser.objects.all()
