# views.py
from rest_framework import status, generics
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Election, Position, Candidate, Voter
from .serializers import (
    LoginSerializer, SignupSerializer, 
    ElectionSerializer, PositionSerializer, 
    CandidateSerializer, ElectionDetailSerializer
)
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .schemas import (
    signup_schema, login_schema,
    create_candidate_schema, create_election_schema,
    create_position_schema, update_candidate_schema, 
    update_election_schema, update_position_schema,
    list_candidates_schema, list_elections_schema,
    list_positions_schema, get_election_schema,
)

class SignupView(APIView):
    permission_classes = [AllowAny]  # Anyone can sign up

    @signup_schema
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "Registration successful"
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  

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
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateElectionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ElectionSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class UpdateElectionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ElectionSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Election.objects.filter(host=self.request.user)


class ElectionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ElectionDetailSerializer

    def get_queryset(self):
        return Election.objects.filter(host=self.request.user)


class ElectionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ElectionDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Election.objects.filter(host=self.request.user)


class AddPositionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PositionSerializer

    def get_queryset(self):
        return Position.objects.filter(election__host=self.request.user)


class UpdatePositionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PositionSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Position.objects.filter(election__host=self.request.user)


class PositionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PositionSerializer

    def get_queryset(self):
        return Position.objects.filter(election__host=self.request.user)


class AddCandidateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CandidateSerializer

    def get_queryset(self):
        return Candidate.objects.filter(election__host=self.request.user)


class UpdateCandidateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CandidateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Candidate.objects.filter(election__host=self.request.user)


class CandidateListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CandidateSerializer

    def get_queryset(self):
        return Candidate.objects.filter(election__host=self.request.user)
