from django.urls import path
from .views import SingUpView, ConfirmCodeView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

app_name = 'users'

urlpatterns = [
    path('signup/', SingUpView.as_view(), name='signup'),
    path('confirm/', ConfirmCodeView.as_view(), name='confirm'),
    path('reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]