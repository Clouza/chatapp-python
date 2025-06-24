from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('register/', views.register, name='register'),
    path('fetch/<int:user_id>/', views.fetch_messages, name='fetch_messages'),
]