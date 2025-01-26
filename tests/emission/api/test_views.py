import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
def test_post_energy_consumptions_success(authenticate_user, payload):
    url = reverse('emission:emission_calc')
    response = authenticate_user.post(url, data=payload, format='json')
    excepted = [
    {
        "name": "SCOPE_1",
        "label": "Brenn-/Treibstoffe, Kältemittel, Prozessemissionen",
        "energy": 93967.5,
        "co2": 26.58484,
        "children": [
            {
                "name": "1.1",
                "label": "Brennstoffe / Wärme",
                "energy": 93967.5,
                "co2": 26.58484,
                "children": [
                    {
                        "name": "1.1.1",
                        "label": "Heizöl leicht (Heating oil usage)",
                        "energy": 27637.5,
                        "co2": 7.7385,
                        "children": []
                    },
                    {
                        "name": "1.1.2",
                        "label": "Heizöl leicht (Heating oil usage)",
                        "energy": 66330.0,
                        "co2": 18.84634,
                        "children": []
                    }
                ]
            }
        ]
    }
]
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == excepted


@pytest.mark.django_db
def test_post_energy_consumptions_unauthenticated(api_client, payload):
    url = reverse('emission:emission_calc') 
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_post_energy_consumptions_invalid_data(authenticate_user, payload):
    url = reverse('emission:emission_calc')
