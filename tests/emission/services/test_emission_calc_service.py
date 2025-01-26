from emission.services.EmssionCalcService.service import EmissionCalcService


def test_execute_returns_correct_emission_tree(sample_energy_consumptions):
    service = EmissionCalcService(energy_consumptions=sample_energy_consumptions)

    result = service.execute()

    expected = [
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
                            "children": [],
                        },
                        {
                            "name": "1.1.2",
                            "label": "Heizöl leicht (Heating oil usage)",
                            "energy": 66330.0,
                            "co2": 18.84634,
                            "children": [],
                        },
                    ],
                }
            ],
        }
    ]

    assert result == expected


def test_execute_with_empty_energy_consumptions():
    service = EmissionCalcService(
        energy_consumptions=[],
    )

    result = service.execute()

    expected = []

    assert result == expected

def test_execute_with_wrong_energy_source_id(sample_energy_consumptions):
    pass