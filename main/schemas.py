from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import serializers
from .serializers import CandidateSerializer, SignupSerializer, LoginSerializer

# Authentication Schemas

signup_schema = extend_schema(
    summary="User Signup",
    description="Registers a new user and returns a JWT token.",
    request=SignupSerializer,
    responses={
        201: {
            "type": "object",
            "properties": {
                "token": {"type": "string"},
                "refresh": {"type": "string"},
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                        "email": {"type": "string"},
                        "role": {"type": "string"},
                    },
                },
            },
        },
        400: {"description": "Invalid input data"},
    },
)

login_schema = extend_schema(
    summary="User Login",
    description="Authenticates a user and returns a JWT token.",
    request=LoginSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "token": {"type": "string"},
                "refresh": {"type": "string"},
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                        "email": {"type": "string"},
                        "role": {"type": "string"},
                    },
                },
            },
        },
        400: {"description": "Invalid credentials"},
    },
)

candidate_schema = extend_schema(
    summary="Candidate Management",
    description="CRUD operations for candidates.",
    request=CandidateSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "position": {"type": "string"},
                "votes": {"type": "integer"},
                "date_added": {"type": "string", "format": "date-time"},
            },
        },
        400: {"description": "Invalid input data"},
    },
)