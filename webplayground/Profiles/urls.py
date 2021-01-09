from django.urls import path
from .views import ProfilesListView, ProfilesDetailView

app_name="app_profiles"

urlpatterns = [
    path('', ProfilesListView.as_view(), name="ProfilesListView"),
    #path('<int:pk>/<slug:user>/', views.ProfilesDetailView.as_view(), name="ProfilesDetailView"),
    path('<username>/', ProfilesDetailView.as_view(), name="ProfilesDetailView"),
]