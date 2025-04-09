from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from .models import Election, Position, Candidate, Voter


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if value.isdigit():
            raise serializers.ValidationError("Password cannot be entirely numeric.")
        return value

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


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'
        read_only_fields = ('host',)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


# Read serializers (nested data for detailed views)

class CandidateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class PositionReadSerializer(serializers.ModelSerializer):
    candidates = CandidateReadSerializer(many=True, read_only=True)

    class Meta:
        model = Position
        fields = '__all__'


class ElectionDetailSerializer(serializers.ModelSerializer):
    positions = PositionReadSerializer(many=True, read_only=True)
    candidates = CandidateReadSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = '__all__'