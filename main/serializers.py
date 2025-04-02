from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from .models import Election, Position, Candidate, Voter


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def raise_validation_error(self, errors):
        raise serializers.ValidationError({"error": errors})

    def validate(self, data):
        errors = {}

        # Explicitly check for existing email
        if User.objects.filter(email=data.get("email")).exists():
            errors["email"] = ["Email is already registered"]

        if errors:
            self.raise_validation_error(errors)

        return data




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def raise_validation_error(self, errors):
        raise serializers.ValidationError({"error": errors})

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                self.raise_validation_error(["Invalid username or password"])

            data["user"] = user
        else:
            self.raise_validation_error(["Both username and password are required"])

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
    position = PositionSerializer()  # Include position details

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
