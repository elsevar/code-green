import json
import os
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
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    json_file = os.path.join(data_folder, 'scopes.json')
    with open(json_file, "r", encoding="utf-8") as f:
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

    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    json_file = os.path.join(data_folder, 'energy-source.json')
    with open(json_file, "r", encoding="utf-8") as f:
        sources_data = json.load(f)

    return [_create_energy_source_from_dict(source_data) for source_data in sources_data]


def find_energy_source_by_id(id: str, sources: list[EnergySource]) -> Optional[EnergySource]:
    for es in sources:
        if es.energy_source_id == id:
            return es

    return None
