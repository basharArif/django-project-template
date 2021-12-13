from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from base import constant
from base.forms import NewUserForm


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            return redirect("base:home")
        else:
            messages.warning(request, 'Your username and password is invalid')

    context = {}
    return render(request, 'accounts/log-in.html', context)


def create_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')

            if user_type == str(constant.OPERATOR):
                user.is_operator = True

            elif user_type == str(constant.ACCOUNTANT):
                user.is_accountant = True
            user.save()

            user = authenticate(request, email=email, password=password)
            login(request, user)
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email

            return redirect("home:home_view")
        else:
            messages.warning(request, 'Your username or password is invalid')
    else:
        form = NewUserForm()

    context = {'form': form}
    return render(request, 'accounts/sign-up.html', context)


def logout_user(request):
    logout(request)
    return redirect('base:login')


def home(request):
    return render(request, 'home/home.html')
