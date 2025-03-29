from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from .models import Election, Position, Candidate, Voter


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password")

            data["user"] = user
        else:
            raise serializers.ValidationError("Both username and password are required")

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


# Serializer for the Position model
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'title', 'election']

# Serializer for the Candidate model
class CandidateSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)  # Include position details

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'position', 'votes', 'date_added', 'election']

# Serializer for the Election model
class ElectionSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)  # Accept host ID for write
    host_details = UserSerializer(source='host', read_only=True)  # Fetch full details for read
    positions = PositionSerializer(many=True, read_only=True)  # Nested positions
    candidates = CandidateSerializer(many=True, read_only=True)  # Nested candidates

    class Meta:
        model = Election
        fields = [
            'id', 'name', 'host', 'host_details', 'is_ended', 'is_started', 
            'date_added', 'positions', 'candidates'
        ]


# Serializer for the Voter model
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = [
            'id', 'election', 'voting_id', 'email', 'student_id', 
            'is_voted', 'date_joined'
        ]
