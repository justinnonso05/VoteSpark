# views.py
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Election, Position, Candidate, Voter
from .serializers import (
    ElectionSerializer, LoginSerializer, PositionSerializer,
    CandidateSerializer, SignupSerializer, VoterSerializer
)
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .schemas import signup_schema, login_schema, candidate_schema

class SignupView(APIView):
    permission_classes = [AllowAny]  # Anyone can sign up

    @signup_schema
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT Token on signup
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "token": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Anyone can log in

    @login_schema
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Generate JWT Token on login
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "token": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ViewSet for Election
class ElectionView(CreateAPIView):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer

# ViewSet for Position
class PositionView(APIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

# ViewSet for Candidate
class CandidateView(APIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    @candidate_schema
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

# ViewSet for Voter
class VoterView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
