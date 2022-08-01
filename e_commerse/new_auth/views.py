from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm
from base.models import Customer


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print(username, password)
            Customer.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('store')
        messages.error(request, 'Unsuccessful registration. Information is invalid')
    form = NewUserForm()
    return render(request, 'new_auth/register.html', context={'form': form})


def new_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        user = authenticate(request, username=username, password=password)
        print('User', user)
        if user is not None:
            login(request, user)
            messages.info(request, f'You are now logged in as {username}.')
            return redirect('store')
        else:
            form = AuthenticationForm()
            messages.error(request, 'Invalid username or password')

    form = AuthenticationForm()
    return render(request, 'new_auth/login.html', context={'form': form})


def new_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out')
    return redirect('store')
