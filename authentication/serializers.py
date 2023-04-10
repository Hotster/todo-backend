from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class UserRegistrationSerializer(serializers.Serializer):

    username = serializers.CharField(min_length=3,
                                     max_length=18,
                                     validators=[RegexValidator(
                                         regex='^[a-zA-Z0-9_-]+$',
                                         message='Username can only contain letters, numbers, underscores and dashes',
                                         code='invalid_username')])
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password'},
                                     validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True,
                                             required=True,
                                             style={'input_type': 'password'})

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A username with this username already exists.')
        return value

    def validate_confirm_password(self, value):
        if value != self.initial_data['password']:
            raise serializers.ValidationError('The passwords do not match.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.get('username'),
                                        password=validated_data.get('password'))
        return user


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
