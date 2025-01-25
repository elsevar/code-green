from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class EnergyConsumption:
    description: str
    energy_source_id: str
    energy_consumption: float
    emission_factor: Optional[float] = None


@dataclass
class EnergySource:
    energy_source_id: int
    scope_id: str
    name: str
    conversion_factor: float
    emission_factor: float


@dataclass
class EnergyScope:
    id: str
    name: str
    label: str
    sub_scopes: List["EnergyScope"] = field(default_factory=list)


@dataclass
class EmissionNode:
    name: str
    label: str
    energy: float = 0.0
    co2: float = 0.0
    children: List["EmissionNode"] = field(default_factory=list)

    def add_child(self, child: "EmissionNode"):
        self.energy += child.energy
        self.co2 += child.co2
        self.children.append(child)