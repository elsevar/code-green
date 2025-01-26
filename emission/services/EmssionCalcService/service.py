from .utils import fetch_scopes, fetch_sources, find_energy_source_by_id
from .dataclasses import EnergyConsumption, EmissionNode, EnergyScope, EnergySource
from typing import Optional
from collections import defaultdict
from dataclasses import asdict


class EmissionCalcService:
    def __init__(
        self,
        energy_consumptions: list[EnergyConsumption],
        scopes: list[EnergyScope] = None,
        sources: list[EnergySource] = None,
    ):
        self._scopes = scopes if scopes else fetch_scopes()
        self._sources = sources if sources else fetch_sources()
        self._energy_consumptions = energy_consumptions

    def execute(self) -> Optional[dict]:
        """
        Build an emission tree from the given energy consumption records.
        """
        emission_leaves = self._build_scope_leaf_map()
        emission_tree = self._build_emission_tree(emission_leaves.keys())
        emission_tree_with_leaves = self._attach_leaf_nodes_to_tree(emission_tree, emission_leaves)
        return self._build_result_dict(emission_tree_with_leaves)

    def _build_result_dict(self, leaves) -> dict:
        """
        Return the computed emission tree as a list of dictionaries.
        """
        emission_tree_as_dict = []
        if leaves:
            emission_tree_as_dict = [asdict(item) for item in leaves]
        return emission_tree_as_dict

    def _build_scope_leaf_map(self) -> Optional[dict[list[EnergyConsumption]]]:
        scopped_leaves = defaultdict(list)
        for energy_consumption in self._energy_consumptions:
            energy_source = find_energy_source_by_id(energy_consumption.energy_source_id, self._sources)
            scope_id = energy_source.scope_id
            scope_leaf_count = len(scopped_leaves[scope_id])
            leaf = self._build_leaf_node(scope_leaf_count, energy_consumption, energy_source)
            scopped_leaves[scope_id].append(leaf)
        return scopped_leaves

    def _build_leaf_node(
        self,
        scope_leaf_count: int,
        energy_consumption: EnergyConsumption,
        energy_source: EnergySource,
    ):
        emission_factor = energy_consumption.emission_factor or energy_source.emission_factor
        energy_value = self._calculate_energy_value(
            energy_consumption.energy_consumption, energy_source.conversion_factor
        )
        co2_value = self._calculate_co2_value(energy_value, emission_factor)
        return EmissionNode(
            name=self._build_leaf_node_name(scope_leaf_count, energy_source.scope_id),
            label=self._build_leaf_node_label(energy_source.name, energy_consumption.description),
            energy=energy_value,
            co2=co2_value,
        )

    def _build_leaf_node_name(self, scope_leaf_count: int, scope_id: str) -> str:
        scope_leaf_count += 1
        return f"{self._scope_id_to_dotted_notation(scope_id)}.{scope_leaf_count}"

    def _build_leaf_node_label(self, energy_source_name: str, energy_consumption_desc: str) -> str:
        return f"{energy_source_name} ({energy_consumption_desc})"

    def _calculate_energy_value(self, energy_consumption: float, conversion_factor: float) -> float:
        return round(energy_consumption * conversion_factor, 5)

    def _calculate_co2_value(self, energy_value: float, emission_factor: float) -> float:
        return round(energy_value * emission_factor / 1000, 5)

    def _scope_id_to_dotted_notation(self, scope_id: str) -> str:
        scope_id_components = scope_id.split("_")
        return f"{scope_id_components[1]}.{scope_id_components[2]}"

    def _build_emission_tree(
        self, scope_ids: list[str], scopes: Optional[list[EnergyScope]] = None
    ) -> Optional[list[EmissionNode]]:
        emision_values: list[EmissionNode] = []
        scopes = scopes or self._scopes
        for scope in scopes:
            if self._scope_prefix_matches_any(scope.id, scope_ids):
                emision_value = EmissionNode(name=scope.id, label=scope.label, energy=0.0, co2=0.0, children=[])
                if scope.sub_scopes:
                    emision_value.children = self._build_emission_tree(scope_ids, scope.sub_scopes)
                emision_values.append(emision_value)
        return emision_values

    def _scope_prefix_matches_any(self, scope_id: str, scopes_ids: set[str]) -> bool:
        if any(s_id.startswith(scope_id) for s_id in scopes_ids):
            return True
        return False

    def _attach_leaf_nodes_to_tree(self, tree: list[EmissionNode], leaves: list[EmissionNode]):
        for node in tree:
            for child in node.children:
                if leaves[child.name]:
                    for leaf in leaves[child.name]:
                        child.add_child(leaf)
                    child.name = self._scope_id_to_dotted_notation(child.name)
                node.energy = node.energy + child.energy
                node.co2 = node.co2 + child.co2
        return tree
