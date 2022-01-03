from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from base import constant
from base.email import send_password_reset_email, send_account_verify_email
from base.forms import NewUserForm, UpdateUserForm, UpdateUserProfileForm
from base.models import CustomUser
from config import settings


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
            if not user.is_verified:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                user_email = user.email
                request.session['uid'] = uid
                request.session['token'] = token
                request.session['user_email'] = user_email
                messages.warning(request, 'Your account is not verified yet. Check email to verify your account or')
            else:
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
            user_type = form.cleaned_data.get('user_type')

            if user_type == str(constant.OPERATOR):
                user.is_operator = True

            elif user_type == str(constant.ACCOUNTANT):
                user.is_accountant = True
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            try:
                send_account_verify_email(request, user.email, uid, token)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('base:user-verification-request')
        else:
            messages.warning(request, 'Your username or password is invalid')
    else:
        form = NewUserForm()

    context = {'form': form}
    return render(request, 'accounts/sign-up.html', context)


def user_verification_request(request):
    return render(request, 'accounts/account_verification_request.html')


def resend_user_verification(request):
    uid = request.session['uid']
    token = request.session['token']
    user_email = request.session['user_email']
    print(uid, token, user_email)

    try:
        send_account_verify_email(request, user_email, uid, token)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return redirect('base:user-verification-request')


def user_verification(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(id=uid)
    except ObjectDoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
    else:
        return HttpResponse('Verification link is invalid!')
    context = {}
    return render(request, 'accounts/account_verification_completed.html', context)


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
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    try:
                        send_password_reset_email(request, user.email, uid, token)
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


def google_login(request):
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse('base:login')
    )
    if 'code' in request.GET:
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        print(params)
        url = 'https://accounts.google.com/o/oauth2/token'
        response = request.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        response = request.get(url, params={'access_token': access_token})
        user_data = response.json()
        email = user_data.get('email')
        if email:
            user = CustomUser.objects.get_or_create(email=email)
            # gender = user_data.get('gender', '').lower()
            # if gender == 'male':
            #     gender = 'M'
            # elif gender == 'female':
            #     gender = 'F'
            # else:
            #     gender = 'O'
            data = {
                'first_name': user_data.get('name', '').split()[0],
                'last_name': user_data.get('family_name'),
                # 'google_avatar': user_data.get('picture'),
                # 'gender': gender,
                'is_active': True
            }
            print(data)
            user.__dict__.update(data)
            user.save()
            user.backend = settings.AUTHENTICATION_BACKENDS
            login(request, user)
        else:
            messages.error(
                request,
                'Unable to login with Gmail Please try again'
            )
        return redirect('base:home')
    # else:
    #     url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
    #     scope = [
    #         "https://www.googleapis.com/auth/userinfo.profile",
    #         "https://www.googleapis.com/auth/userinfo.email"
    #     ]
    #     scope = " ".join(scope)
    #     url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
    #     print(scope)
    #     return redirect(url)
