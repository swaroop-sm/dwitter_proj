from django import template
from dwitter.models import *

register = template.Library()


@register.simple_tag
def like_or_unlike(tweetObj, usrObj):
    custom_usr = usrObj.customuser_set.get()
    if tweetObj.user_has_liked(custom_usr):
        return 'Unlike'
    else:
        return 'Like'


@register.simple_tag
def follow_or_unfollow(rqusrObj, twtusrObj):
    custom_usr = rqusrObj.customuser_set.get()
    if FollowUser.objects.filter(active = 2, following_user = custom_usr, 
            followed = twtusrObj).exists():
        return 'Unfollow'
    else:
        return 'Follow'


@register.simple_tag
def can_user_follow(rqusrObj, twtusrObj):
    if rqusrObj.id == twtusrObj.user.id:
        return False
    else:
        return True