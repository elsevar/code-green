from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import EnergyConsumptionSerializer
from rest_framework import status
from .services.EmssionCalcService.service import EmissionCalcService


class EnergyConsumptionAPIView(APIView):
    """
    API view to handle POST requests for creating multiple EnergyConsumption instances.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        Handle POST request to create multiple EnergyConsumption instances.
        Expects a list of EnergyConsumption items in the request data.
        """
        serializer = EnergyConsumptionSerializer(data=request.data, many=True)
        if serializer.is_valid():
            energy_consumptions = serializer.save() 
            response_data = EmissionCalcService(energy_consumptions).execute()

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)