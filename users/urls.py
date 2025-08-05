from django.urls import path
from .views import Register, ConfirmCodeView, CustomLogoutView, CustomLoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

app_name = 'users'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('confirm/', ConfirmCodeView.as_view(), name='confirm'),
    path('reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]