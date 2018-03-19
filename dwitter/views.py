from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import View
from dwitter.models import *
from constants import *


class HomeView(View):
    
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.filter(active = 2)
        return render(request, "index.html", locals())


class UserTweetView(LoginRequiredMixin, View, BaseView, CSRFExemptMixin):
    login_url = '/signin/'

    def mytweets(self, request, *args, **kwargs):
        user = request.user
        cusr = user.customuser_set.get()
        tweets = cusr.tweet_set.filter(active = 2).order_by('-created_at')
        return render(request, 'mytweets.html', locals())


    def addtweet(self, request, *args, **kwargs):
        user = request.user
        cusr = user.customuser_set.get()
        new_tweet = True
        if request.method == 'POST':
            try:
                tweet_txt = request.POST.get('tweet_txt')

                tweetObj = Tweet(tweet = tweet_txt)
                tweetObj.tweet_by = cusr
                tweetObj.save()

                return HttpResponseRedirect(reverse('mytweets-url'))
            except Exception as e:
                print e.message
                errorlists = {'err': "Something went wrong. Please try again."}

        return render(request, 'add_edit_tweet.html', locals())


    def edittweet(self, request, *args, **kwargs):
        user = request.user
        cusr = user.customuser_set.get()
        new_tweet = False
        tweet_id = kwargs.get('tid')
        tweetObj = Tweet.objects.get(id = tweet_id)
        if request.method == "POST":
            try:
                tweet_txt = request.POST.get('tweet_txt')

                tweetObj.tweet = tweet_txt
                tweetObj.save()

                return HttpResponseRedirect(reverse('mytweets-url'))
            except Exception as e:
                print e.message
                errorlists = {'err': "Something went wrong. Please try again."}

        return render(request, 'add_edit_tweet.html', locals())


class TweetLikeView(LoginRequiredMixin, View, BaseView):
    login_url = '/signin/'

    def liketweet(self, request, *args, **kwargs):
        user = request.user
        success, msg, new_txt = False, '', ''
        cusr = user.customuser_set.get()
        tweet_id = kwargs.get('tid')
        tweetObj = Tweet.objects.get(id = tweet_id)
        
        if request.is_ajax():
            if not TweetLikes.objects.filter(active = 2, liked = tweetObj, liked_by = cusr).exists():
                tweetlikeObj = TweetLikes(liked = tweetObj)
                tweetlikeObj.liked_by = cusr
                tweetlikeObj.save()
                success = True
                new_txt = 'Unlike'
            else:
                msg = "You have already liked this tweet"

            no_of_likes = tweetObj.no_of_likes()
            
            return JsonResponse({'success': success, 'msg': msg, 'new_txt': new_txt,
                    'no_of_likes': no_of_likes,
                    'new_url': reverse('unlike-tweet-json-url', kwargs={'tid': tweet_id})},
                    safe = False)
        else:
            return HttpResponseRedirect(reverse('home-url'))


    def unliketweet(self, request, *args, **kwargs):
        user = request.user
        success, msg, new_txt = False, '', ''
        cusr = user.customuser_set.get()
        tweet_id = kwargs.get('tid')
        tweetObj = Tweet.objects.get(id = tweet_id)
        
        if request.is_ajax():
            if TweetLikes.objects.filter(active = 2, liked = tweetObj, liked_by = cusr).exists():
                tweetlikeObj = TweetLikes.objects.get(active = 2, liked = tweetObj, liked_by = cusr)
                tweetlikeObj.active = 0
                tweetlikeObj.save()
                success = True
                new_txt = 'Like'
            else:
                msg = "You have not liked this tweet"

            no_of_likes = tweetObj.no_of_likes()
            
            return JsonResponse({'success': success, 'msg': msg, 'new_txt': new_txt,
                            'no_of_likes': no_of_likes,
                            'new_url': reverse('like-tweet-json-url', kwargs={'tid': tweet_id})},
                            safe = False)
        else:
            return HttpResponseRedirect(reverse('home-url'))
