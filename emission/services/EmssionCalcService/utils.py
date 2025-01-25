import json
from typing import Optional
from emission.services.EmssionCalcService.dataclasses import EnergyScope, EnergySource


def _create_energy_scope_from_dict(data: dict) -> EnergyScope:
    return EnergyScope(
        id=data["id"],
        name=data["name"],
        label=data["label"],
        sub_scopes=[_create_energy_scope_from_dict(sub) for sub in data.get("subScopes", [])],
    )


def fetch_scopes():
    with open("data/scopes.json", "r", encoding="utf-8") as f:
        scopes_data = json.load(f)

    return [_create_energy_scope_from_dict(scope_data) for scope_data in scopes_data]


def _create_energy_source_from_dict(data: dict) -> EnergySource:
    return EnergySource(
        energy_source_id=data["energySourceId"],
        scope_id=data["scopeId"],
        name=data["name"],
        conversion_factor=float(data["conversionFactor"]),
        emission_factor=float(data["emissionFactor"]),
    )


def fetch_sources():
    with open("data/energy-source.json", "r", encoding="utf-8") as f:
        sources_data = json.load(f)

    return [_create_energy_source_from_dict(source_data) for source_data in sources_data]


def find_energy_source_by_id(id: str, sources: list[EnergySource]) -> Optional[EnergySource]:
    for es in sources:
        if es.energy_source_id == id:
            return es

    return None
