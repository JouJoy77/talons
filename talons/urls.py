"""talons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from main import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from users import views as user_views
from search import views as search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'home'),
    path('price', views.view_price, name = 'price'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('cart/', include('cart.urls'), name='cart'),
    path('search/', include('search.urls', namespace='search')),
    path('confirm_use/', user_views.ConfirmUseTicket.as_view(template_name='users/profile.html'), name='confirm_use')

]
