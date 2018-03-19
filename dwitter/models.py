from __future__ import unicode_literals

from django.db import models
from main_app.models import *
from user_app.models import CustomUser

# Create your models here.

class Tweet(BaseModel):

    tweet = models.TextField("Tweet")
    tweet_by = models.ForeignKey(CustomUser)

    def __unicode__(self):
        return "%s | %s" %(self.tweet[:10], self.tweet_by.user.username)

    def no_of_likes(self):
        return self.tweetlikes_set.filter(active = 2).count()

    def user_has_liked(self, cuser):
        if self.tweetlikes_set.filter(active = 2, liked_by = cuser).exists():
            return True
        else:
            return False

class TweetLikes(BaseModel):

    liked = models.ForeignKey(Tweet)
    liked_by = models.ForeignKey(CustomUser)

