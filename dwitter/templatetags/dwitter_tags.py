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
