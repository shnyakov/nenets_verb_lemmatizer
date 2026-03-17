from django.urls import include, path

urlpatterns = [
    path("", include("lemmatizer_app.urls")),
]
