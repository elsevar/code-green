from rest_framework import serializers
from .services.EmssionCalcService.dataclasses import EnergyConsumption


class EnergyConsumptionSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)
    energy_source_id = serializers.CharField(max_length=100)
    energy_consumption = serializers.FloatField()
    emission_factor = serializers.FloatField(required=False, allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `EnergyConsumption` instance, given the validated data.
        """
        return EnergyConsumption(**validated_data)