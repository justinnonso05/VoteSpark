from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import serializers
from .serializers import CandidateSerializer, SignupSerializer, LoginSerializer, ElectionSerializer, PositionSerializer
from drf_yasg.utils import swagger_auto_schema

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


create_election_schema = swagger_auto_schema(
    operation_description="Create a new election",
    request_body=ElectionSerializer,
    responses={201: ElectionSerializer}
)

update_election_schema = swagger_auto_schema(
    operation_description="Update an election",
    request_body=ElectionSerializer,
    responses={200: ElectionSerializer}
)

get_election_schema = swagger_auto_schema(
    operation_description="Retrieve an election",
    responses={200: ElectionSerializer}
)

list_elections_schema = swagger_auto_schema(
    operation_description="List all elections",
    responses={200: ElectionSerializer(many=True)}
)


create_position_schema = swagger_auto_schema(
    operation_description="Add a new position",
    request_body=PositionSerializer,
    responses={201: PositionSerializer}
)

update_position_schema = swagger_auto_schema(
    operation_description="Update a position",
    request_body=PositionSerializer,
    responses={200: PositionSerializer}
)

list_positions_schema = swagger_auto_schema(
    operation_description="List all positions",
    responses={200: PositionSerializer(many=True)}
)


create_candidate_schema = swagger_auto_schema(
    operation_description="Add a new candidate",
    request_body=CandidateSerializer,
    responses={201: CandidateSerializer}
)

update_candidate_schema = swagger_auto_schema(
    operation_description="Update a candidate",
    request_body=CandidateSerializer,
    responses={200: CandidateSerializer}
)

list_candidates_schema = swagger_auto_schema(
    operation_description="List all candidates",
    responses={200: CandidateSerializer(many=True)}
)
