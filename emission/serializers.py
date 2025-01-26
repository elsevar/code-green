from rest_framework import serializers
from .services.EmssionCalcService.dataclasses import EnergyConsumption


class EnergyConsumptionSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)
    energy_source_id = serializers.CharField(max_length=100)
    energy_consumption =  serializers.DecimalField(
        max_digits=15,
        decimal_places=5,
        coerce_to_string=False) 
    emission_factor = serializers.DecimalField(
        max_digits=10,
        decimal_places=5,
        required=False,
        allow_null=True,
        coerce_to_string=False)

    def create(self, validated_data):
        """
        Create and return a new `EnergyConsumption` instance, given the validated data.
        """
        return EnergyConsumption(
            description=validated_data['description'],
            energy_source_id=validated_data['energy_source_id'],
            energy_consumption=float(validated_data['energy_consumption']),
            emission_factor=float(validated_data['emission_factor']) if validated_data.get('emission_factor') is not None else None
        )