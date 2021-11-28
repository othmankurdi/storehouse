from datetime import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from storehouse.forms import SignupForm
from storehouse.models import User
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


class UserView:

    def signup(request):
        if request.method == 'POST':
            signup_form = SignupForm(request.POST)
            signup_form.email = request.POST['email']
            signup_form.full_name = request.POST['full_name']
            new_user = User()
            new_user.full_name = request.POST['full_name']
            new_user.email = request.POST['email']
            new_user.age = request.POST['age']
            new_user.phone = request.POST['phone']
            new_user.bio = request.POST['bio']
            new_user.create_date = datetime.now()
            if signup_form.is_valid():
                auth_user = signup_form.save()
                new_user.auth_user = auth_user
                new_user.save()
                messages.info(request, "Thanks for registering. You are now logged in.")
                new_user = authenticate(username=signup_form.cleaned_data['username'],
                                        password=signup_form.cleaned_data['password1'],
                                        )
                login(request, new_user)
                return HttpResponseRedirect("/storehouse/products")
        elif request.method == 'GET':
            signup_form = SignupForm()
        return render(request, 'storehouse/signup.html', {'form': signup_form})

    def login(request):
        if request.method == 'POST':
            postdata = request.POST.copy()
            username = postdata.get('username', '')
            password = postdata.get('password', '')
            try:
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect("/storehouse/products")
            except:
                messages.error(request, 'username or password not correct')
                return redirect("/storehouse/login/")
        elif request.method == 'GET':
            form = AuthenticationForm()
            return render(request, 'storehouse/login.html', {'form': form})


    def logout(request):
        logout(request)
        return redirect('storehouse:login')

    def edit_profile(request):
        if request.method == 'GET':
            return render(request, 'storehouse/edit_profile.html',
                          {'userinfo': User.objects.get(auth_user_id=request.user.id),
                           'authuserinfo': request.user,
                           'user_name': request.user.username}, )
        elif request.method == 'POST':
            storehouse_user = User.objects.get(auth_user_id=request.user.id)
            auth_user = request.user
            storehouse_user.full_name = request.POST.get('full_name')
            storehouse_user.email = request.POST.get('email')
            storehouse_user.age = request.POST.get('age')
            storehouse_user.phone = request.POST.get('phone')
            storehouse_user.bio = request.POST.get('bio')
            auth_user.username = request.POST.get('username')
            auth_user.password = request.POST.get('password')
            auth_user.email = request.POST.get('email')
            storehouse_user.save()
            auth_user.save()
            return render(request, 'storehouse/profile.html',
                          {'userinfo': User.objects.get(auth_user_id=request.user.id),
                           'authuserinfo': request.user,
                           'user_name': request.user.username}, )

    def view_profile(request):
        if request.method == 'GET':
            return render(request, 'storehouse/profile.html',
                          {'storehouseuserinfo': User.objects.get(auth_user_id=request.user.id),
                           'authuserinfo': request.user,
                           'user_name': request.user.username}, )
        elif request.method == 'POST':
            return render(request, 'storehouse/profile.html')
