"""
URL configuration for TomikoTradeProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, "custom_404.html", status=404)

handler404 = custom_404

urlpatterns = [
    path("", include("TomikoApp.urls")),
    path("economy/", include("TomikoApp.urls")),
    path("catalog/", include("TomikoApp.urls")),
    path("card/", include("TomikoApp.urls")),
    path("contacts/", include("TomikoApp.urls")),
    path("politicy/", include("TomikoApp.urls")),
    path("akcii/", include("TomikoApp.urls")),
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('cars/', include('cars.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
