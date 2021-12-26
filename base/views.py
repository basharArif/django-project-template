from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from base import constant
from base.forms import NewUserForm, UpdateUserForm, UpdateUserProfileForm
from base.models import CustomUser


@login_required
def home(request):
    return render(request, 'home/home.html')


@login_required
def user_profile(request, name):
    return render(request, 'home/profile.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            return redirect('base:home')
        else:
            messages.warning(request, 'Your username or password is invalid')

    context = {
        'form': AuthenticationForm()
    }
    return render(request, 'accounts/log-in.html', context)


def create_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST, request.FILES)
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

            return redirect("base:home")
        else:
            messages.warning(request, 'Your username or password is invalid')
    else:
        form = NewUserForm()

    context = {'form': form}
    return render(request, 'accounts/sign-up.html', context)


def logout_user(request):
    logout(request)
    return redirect('base:login')


def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_user = CustomUser.objects.filter(Q(email=data))
            if associated_user.exists():
                for user in associated_user:
                    subject = 'Password Reset Request'
                    email_template_name = 'accounts/password_reset_email.txt'
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("base:password-reset-done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/reset-password.html",
                  context={"password_reset_form": password_reset_form})


def update_user_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        user_profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()

            messages.success(request, 'Your profile is updated successfully')
            return redirect('base:profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        user_profile_form = UpdateUserProfileForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form
    }

    return render(request, 'home/edit_profile.html', context)


def profile(request):
    context = {
        'profile': request.user.userprofile
    }
    return render(request, 'home/profile.html', context)
