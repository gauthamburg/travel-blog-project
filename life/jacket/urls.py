from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('create-post/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('create-location/', views.create_location_view, name='create_location'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('search/', views.search_view, name='search'),
]