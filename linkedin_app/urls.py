from django.urls import path
from . import views

urlpatterns = [
    path('', views.linkedin_login_and_scrape, name='linkedin_login'),
]
