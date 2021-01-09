from django.urls import path
from . import views

app_name = "app_pages"

urlpatterns = [
    path('', views.PageListView.as_view(), name='PageListView'),
    #path('', views.pages, name="pages"),
    #path('<int:page_id>/<str:page_title>/', views.page, name='page'),
    path('<int:pk>/<str:page_title>', views.PageDetailView.as_view(), name="PageDetailView"),
    path('create/', views.PageCreate.as_view(), name="PageCreate"),
    path('update/<int:pk>/<str:page_title>/', views.PageUpdate.as_view(), name="PageUpdate"),
    path('delete/<int:pk>/<str:page_title>/', views.PageDelete.as_view(), name="PageDelete"),
]