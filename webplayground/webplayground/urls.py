"""webplayground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("core.urls")),
    path('pages/', include("pages.urls")),
    path('accounts/', include("django.contrib.auth.urls")), # Para gestionar el "Login y Logout".
    path('accounts/', include("registration.urls")),
    path('profiles/', include("Profiles.urls")),
    path('messenger/', include("messenger.urls")),
    path('admin/', admin.site.urls),
]

# Configuramos la carga de los ficheros "media":
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)