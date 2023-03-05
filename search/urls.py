from django.urls import path
 
from . import views
from users import views as user_views

app_name = 'search'

urlpatterns = [
    path('index/', views.ESearchView.as_view(template_name='search/index.html'), name='index'),
    path('delete/', views.DeleteObject.as_view(template_name='search/index.html'),name='delete'),
]