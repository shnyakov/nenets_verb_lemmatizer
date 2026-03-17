from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/lemmatize/", views.api_lemmatize, name="api-lemmatize"),
    path("health/", views.health, name="health"),
]
