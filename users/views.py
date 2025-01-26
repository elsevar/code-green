from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.db.utils import IntegrityError
from .serializers import UserSerializer

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "User authorized successfully.",
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                })
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SignupView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except IntegrityError:
                return Response({
                    "message": "Sorry, that username is unavailable. Please try another one."
                }
                )

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully.",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)