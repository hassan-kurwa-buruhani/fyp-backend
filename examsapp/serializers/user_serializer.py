from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from examsapp.models import Roles
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from math import radians, cos, sin, asin, sqrt

User = get_user_model()

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    Returns distance in meters.
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000  # Radius of earth in meters
    return c * r

from rest_framework import serializers
from django.conf import settings

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Extract extra fields
        device_id = self.context['request'].data.get('device_id')
        latitude = self.context['request'].data.get('latitude')
        longitude = self.context['request'].data.get('longitude')

        # Validate username and password first
        data = super().validate(attrs)

        user = self.user

        # Only enforce location and device checks for non-students
        if user.role != 'Student':
            # Check device_id provided
            if not device_id:
                raise serializers.ValidationError("Device ID is required for your role.")

            # Validate location provided
            if latitude is None or longitude is None:
                raise serializers.ValidationError("Location (latitude and longitude) is required for your role.")

            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                raise serializers.ValidationError("Invalid latitude or longitude.")

            # Check if location is within campus radius
            distance = haversine(
                longitude, latitude,
                settings.CAMPUS_CENTER['lng'], settings.CAMPUS_CENTER['lat']
            )
            print(f"Distance from campus center: {distance} meters")
            if distance > settings.CAMPUS_RADIUS_METERS:
                raise serializers.ValidationError("You must be on campus to log in.")

            # Device binding logic
            if user.device_id is None:
                # First login, bind device
                user.device_id = device_id
                user.save(update_fields=['device_id'])
            elif user.device_id != device_id:
                raise serializers.ValidationError("This device is not authorized for your account.")

        # For students, no extra checks; login with username and password only

        # Optionally, add role to token response
        data['id'] = user.id
        data['username'] = user.username
        data['role'] = user.role
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        return data
    




# student registration serializer
class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # For password confirmation

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=Roles.STUDENT  # Force role to Student
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    new_password = serializers.CharField(write_only=True, required=False)
    verify_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'new_password', 'verify_password')

    def validate(self, data):
        new_password = data.get('new_password')
        verify_password = data.get('verify_password')

        # If either is provided, both must be present and match
        if new_password or verify_password:
            if not new_password:
                raise serializers.ValidationError({"new_password": "This field is required."})
            if not verify_password:
                raise serializers.ValidationError({"verify_password": "This field is required."})
            if new_password != verify_password:
                raise serializers.ValidationError({"verify_password": "Passwords do not match."})
            if len(new_password) < 4:
                raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long."})

        return data

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('verify_password', None)  # Remove it; only used for validation

        # Update fields like first_name, last_name, etc.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If new_password was provided, update password
        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance
