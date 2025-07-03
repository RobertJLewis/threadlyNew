"""
URL configuration for blogsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from blog import views 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from blog.views import register, CategoryThreadList, ThreadDetail, comment_on_thread, react_to_thread, logout_view
from django.views.generic import TemplateView

urlpatterns = [
    path("",       views.home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/login/", LoginView.as_view(template_name="account/login.html"), name="login"),
    path("accounts/register/", register, name="register"),
    path("privacy/", TemplateView.as_view(template_name="privacy.html"), name="privacy"),
    path("terms/",   TemplateView.as_view(template_name="terms.html"),  name="terms"),
    path("category/<slug:slug>/", CategoryThreadList.as_view(), name="category_feed"),
    path("thread/<int:pk>/", ThreadDetail.as_view(),   name="thread_detail"),
    path("thread/<int:pk>/comment/", comment_on_thread, name="thread_comment"),
    path("thread/<int:pk>/react/",   react_to_thread,   name="thread_react"),
    path("logout/", logout_view, name="logout"),
]

# Serve uploaded media during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)