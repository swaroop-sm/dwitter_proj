from __future__ import unicode_literals

from django.db import models
from main_app.models import *
from user_app.models import CustomUser

# Create your models here.

class Tweet(BaseModel):

    tweet = models.TextField("Tweet")
    tweet_by = models.ForeignKey(CustomUser)



class TweetLikes(BaseModel):

    liked = models.ForeignKey(Tweet)
    liked_by = models.ForeignKey(CustomUser)

