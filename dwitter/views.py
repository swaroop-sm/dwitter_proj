from django.shortcuts import render
from django.views import View
from dwitter.models import *


class HomeView(View):
    
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.filter(active = 2)
        return render(request, "index.html", locals())
