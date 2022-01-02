from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.update_user_profile, name='update-profile'),
    path('register/', views.create_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('password_reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password-reset-done"),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password-reset-confirm.html"),
         name="password-reset-confirm"),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html")),
    path('password_reset', views.password_reset_request, name='password-reset'),
    path('password_change', auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"),
         name="password-change"),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_complete.html"),
         name="password-change-done"),
    path('verification/message', views.user_verification_request, name='user-verification-request'),
    path('verification/<uidb64>/<token>', views.user_verification, name='account-verification'),
    path('verification/resend', views.resend_user_verification, name='resend-verification'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
