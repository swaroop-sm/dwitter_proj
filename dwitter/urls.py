from django.conf.urls import url
from dwitter.views import *


urlpatterns = [
    url(r'^$', HomeView.as_view(),
            name = 'home-url'),

    url(r'^tweet/mytweets/$', UserTweetView.as_view(action = "mytweets"),
            name = 'mytweets-url'),

    url(r'^tweet/add-tweet/$', UserTweetView.as_view(action = "addtweet"),
            name = 'add-tweet-url'),

    url(r'^tweet/edit-tweet/(?P<tid>[0-9]+)/$', UserTweetView.as_view(action = "edittweet"),
            name = 'edit-tweet-url'),

    url(r'^tweet/like-tweet/(?P<tid>[0-9]+)/$', TweetLikeView.as_view(action = "liketweet"),
            name = 'like-tweet-json-url'),

    url(r'^tweet/unlike-tweet/(?P<tid>[0-9]+)/$', TweetLikeView.as_view(action = "unliketweet"),
            name = 'unlike-tweet-json-url'),    
]