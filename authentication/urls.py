from django.contrib.auth.views import LogoutView
from django.urls import path

from authentication.views import UserLoginView, UserRegistrationView, GetCSRFToken, IsAuthenticatedView

urlpatterns = [
    path('login', UserLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('register', UserRegistrationView.as_view()),
    path('is_authenticated', IsAuthenticatedView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
]
