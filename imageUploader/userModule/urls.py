from django.urls import path

from . import views

urlpatterns = [
    path('baseurl/api/v1/create-user',  views.create_user, name='create-user'),
    path('baseurl/api/v1/all-user', views.fetch_all, name='fetch-all-users')
]
