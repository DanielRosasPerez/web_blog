from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate

app_name = "app_registration"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="SignUpView"),
    path('profile/', ProfileUpdate.as_view(), name="ProfileUpdate"),
    path('profile/email/', EmailUpdate.as_view(), name="ProfileEmail"),
]