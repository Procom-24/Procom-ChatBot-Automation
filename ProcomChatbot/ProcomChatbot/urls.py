"""
URL configuration for ProcomChatbot project.

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

urlpatterns = [
    path('admin/jf9sanmcvif9ghk3785jvi83n239$saj392k(sdvnsimvm,30JK28cv2bv5amvm2mios/', admin.site.urls),
    path("", include("ProcomChatbot_App.urls")),
]

handler404 = "ProcomChatbot_App.views.page_not_found_404"
