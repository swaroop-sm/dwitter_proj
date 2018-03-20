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

    url(r'^follow-user/(?P<cuid>[0-9]+)/$', FollowUserView.as_view(action = "follow_user"),
            name = 'follow-user-json-url'),

    url(r'^unfollow-user/(?P<cuid>[0-9]+)/$', FollowUserView.as_view(action = "unfollow_user"),
            name = 'unfollow-user-json-url'),

    url(r'^user-tweets/(?P<uid>[0-9]+)/$', ResultDetailView.as_view(action = "user_tweets"),
            name = "user-tweets-url"),

    url(r'^tweet/(?P<tid>[0-9]+)/$', ResultDetailView.as_view(action = "tweet"),
            name = "tweet-url"),
]