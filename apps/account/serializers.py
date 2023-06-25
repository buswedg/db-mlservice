from django.contrib.auth import authenticate, get_user_model
from django.core.validators import validate_email
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password',)

    def validate_email(self, value):
        if not validate_email(value):
            raise serializers.ValidationError(
                'Invalid email address.'
            )

        return value

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=75)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password', 'tokens',)

    def get_tokens(self, obj):
        user = get_user_model().objects.get(email=obj.email)
        return {'refresh': user.tokens['refresh'], 'access': user.tokens['access']}

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if not email:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if not username:
            raise serializers.ValidationError(
                'A username is required to log in.'
            )

        if not password:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return user


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)


class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'tokens',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance
