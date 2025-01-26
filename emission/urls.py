from django.urls import path
from .views import HelloView

app_name="emission"
urlpatterns = [
    path('', HelloView.as_view(), name="hello"),
]

