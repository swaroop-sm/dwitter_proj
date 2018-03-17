from django.conf.urls import url
from dwitter.views import *


urlpatterns = [
    url(r'^$', HomeView.as_view(),
            name = 'home-url')    
]