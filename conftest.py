from emission.services.EmssionCalcService.dataclasses import EnergyConsumption
import pytest
from dataclasses import asdict
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def sample_energy_consumptions():
    return [
        EnergyConsumption(
            description="Heating oil usage",
            energy_source_id="2001",
            energy_consumption=2500.0,
            emission_factor=0.28,
        ),
        EnergyConsumption(
            description="Heating oil usage",
            energy_source_id="2001",
            energy_consumption=6000.0,
        ),
    ]

@pytest.fixture
def payload(sample_energy_consumptions):
    return [asdict(consmp) for consmp in sample_energy_consumptions]


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_user(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def authenticate_user(api_client, authenticated_user):
    api_client.force_authenticate(user=authenticated_user)
    return api_client