from django.conf.urls import url
from user_app.views import *

urlpatterns = [
    url(r'^sign-up/$', SignupView.as_view(),
                name = 'signup-url'),

    url(r'^signin/$', LoginView.as_view(),
                name = 'signin-url'),

    url(r'^view/myprofile/$', UserView.as_view(action = 'myprofile'),
                name = 'myprofile-url'),

    url(r'^edit/myprofile/$', UserView.as_view(action = 'myprofile_edit'),
                name = 'myprofile-edit-url'),
]