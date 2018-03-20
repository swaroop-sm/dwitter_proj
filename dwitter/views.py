from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views import View
from dwitter.models import *
from constants import *


class HomeView(LoginRequiredMixin, View):
    login_url = '/u/signin/'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        cusr = user.customuser_set.get()
        users = cusr.users_following()
        tweets = Tweet.objects.filter(active = 2, tweet_by__in = users)
        return render(request, "index.html", locals())


    def post(self, request, *args, **kwargs):
        qry = request.POST.get('query')
        
        tweets = Tweet.objects.filter(tweet__icontains = qry)
        users = User.objects.filter(
                    Q(username__icontains = qry) | Q(first_name__icontains = qry) |
                    Q(last_name__icontains = qry) | Q(email__icontains = qry))
        return render(request, 'search_result.html', locals())


class ResultDetailView(LoginRequiredMixin, View, BaseView):
    login_url = '/u/signin/'
    template_name = 'index.html'
    
    def user_tweets(self, request, *args, **kwargs):
        userID = kwargs.get('uid')
        cusr = CustomUser.objects.get(user__id = userID)
        tweets = Tweet.objects.filter(active = 2, tweet_by = cusr)
        return render(request, self.template_name, locals())


    def tweet(self, request, *args, **kwargs):
        tweet_id = kwargs.get('tid')
        tweets = Tweet.objects.filter(id = tweet_id)
        return render(request, self.template_name, locals())


class UserTweetView(LoginRequiredMixin, View, BaseView, CSRFExemptMixin):
    login_url = '/u/signin/'

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
    login_url = '/u/signin/'

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


class FollowUserView(LoginRequiredMixin, View, BaseView):
    login_url = '/u/signin/'

    def follow_user(self, request, *args, **kwargs):
        user = request.user
        cusr = user.customuser_set.get()
        success, msg, new_txt = False, '', ''
        flw_cuid = kwargs.get('cuid')
        flw_cuser = CustomUser.objects.get(id = flw_cuid)

        if request.is_ajax():
            if not FollowUser.objects.filter(active = 2, following_user = cusr, followed = flw_cuser).exists():
                flwusrObj = FollowUser(following_user = cusr)
                flwusrObj.followed = flw_cuser
                flwusrObj.save()

                success = True
                new_txt = 'Unfollow'
            else:
                msg = "You are already following this user."
                        
            return JsonResponse({'success': success, 'msg': msg, 'new_txt': new_txt,
                    'new_url': reverse('unfollow-user-json-url', kwargs={'cuid': flw_cuid})},
                    safe = False)
        else:
            return HttpResponseRedirect(reverse('home-url'))


    def unfollow_user(self, request, *args, **kwargs):
        user = request.user
        success, msg, new_txt = False, '', ''
        cusr = user.customuser_set.get()
        flwg_cuid = kwargs.get('cuid')
        flwg_cuser = CustomUser.objects.get(id = flwg_cuid)
        
        if request.is_ajax():
            if FollowUser.objects.filter(active = 2, following_user = cusr, followed = flwg_cuser).exists():
                flwusrObj = FollowUser.objects.get(active = 2, following_user = cusr, followed = flwg_cuser)
                flwusrObj.active = 0
                flwusrObj.save()
                success = True
                new_txt = 'Follow'
            else:
                msg = "You are not following this user."
            
            return JsonResponse({'success': success, 'msg': msg, 'new_txt': new_txt,
                            'new_url': reverse('follow-user-json-url', kwargs={'cuid': flwg_cuid})},
                            safe = False)
        else:
            return HttpResponseRedirect(reverse('home-url'))



