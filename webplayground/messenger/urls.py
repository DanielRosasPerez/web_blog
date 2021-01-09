from django.urls import path
from .views import ThreadList, ThreadDetailView, add_message, start_thread

app_name = "app_messenger"

urlpatterns = [
    path('', ThreadList.as_view(), name="ThreadList"),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name="ThreadDetailView"), # Recordemos que "pk" siempre es el "id" de la instancia.
    path('thread/<int:pk>/add/', add_message, name="add_message"),
    path('thread/start/<username>/', start_thread, name="start_thread"),
]