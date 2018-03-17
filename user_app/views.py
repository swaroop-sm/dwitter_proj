from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime
from user_app.models import *
from user_app.forms import *
from constants import *


class SignupView(View, CSRFExemptMixin, CustomForm):

    def get_user(self, username):
        try:
            return User.objects.filter(username = username)
        except User.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'signup.html', locals())


    def post(self, request, *args, **kwargs):
        errorlists, success = {}, False
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                
                username = request.POST.get('username')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                password = request.POST.get('password')
                email = request.POST.get('email')
                mobile = request.POST.get('mobile')
                dob = request.POST.get('dob')

                if not self.get_user(username):
                    usr = User.objects.create_user(username, email, password)
                    usr.first_name = first_name
                    usr.last_name = last_name
                    usr.save()

                    custom_usr = CustomUser(user = usr)
                    custom_usr.mobile = mobile
                    custom_usr.dob = datetime.strptime(dob, '%m/%d/%Y')
                    custom_usr.save()

                    success = True
                else:
                    errorlists.update({'err': 'Username already exists.'})
            except Exception as e:
                print e.message
                errorlists.update({'err': 'Something went wrong. Please try after sometime'})
        else:
            errorlists = self.error_to_json(form)
        return render(request, "signup.html", locals())


class LoginView(View, CSRFExemptMixin, CustomForm):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'signin.html', locals())


    def post(self, request, *args, **kwargs):
        errorlists, success = {}, False
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home-url'))
            else:
                errorlists.update({'err': 'Invalid username/password.'})
        else:
            errorlists = self.error_to_json(form)
        return render(request, "signin.html", locals())


class UserView(LoginRequiredMixin, View, BaseView, CSRFExemptMixin):
    login_url = '/signin/'

    def myprofile(self, request, *args, **kwargs):
        user = request.user
        custom_usr = user.customuser_set.get()
        return render(request, 'myprofile.html', locals())


    def myprofile_edit(self, request, *args, **kwargs):
        
        user = request.user
        custom_usr = user.customuser_set.get()
        if request.method == "POST":
            try:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                mobile = request.POST.get('mobile')
                dob = request.POST.get('dob')
                city = request.POST.get('city')
                country = request.POST.get('country')
                gender = request.POST.get('gender')
                
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                custom_usr.mobile = mobile
                custom_usr.dob = datetime.strptime(dob, '%d/%m/%Y')
                custom_usr.city = city
                custom_usr.country = country
                custom_usr.mobile = mobile
                custom_usr.gender = gender
                custom_usr.save()

                return HttpResponseRedirect(reverse('myprofile-url'))
            
            except Exception as e:
                print e.message
                errorlists = {'err': 'Something went wrong. Please try after sometime'}

        return render(request, 'myprofile-edit.html', locals())