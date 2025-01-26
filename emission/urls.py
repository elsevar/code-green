from django.urls import path
from .views import EnergyConsumptionAPIView

app_name="emission"
urlpatterns = [
    path('calc/', EnergyConsumptionAPIView.as_view(), name="emission_calc"),
]

