from rest_framework import serializers
from .models import FootballField, ProfileUser
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class FootballFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballField
        fields = "__all__"


class FootballFieldOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballField
        fields = [
            "id",
            "name",
            "address",
            "contact",
            "bron",
            "date",
            "hourly_price",
            "image",
        ]
        # fields = '__all__'


class FootballFieldBronSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballField
        fields = ["id", "bron", "date"]
        # fields = '__all__'


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            user = ProfileUser(
                username=validated_data["username"], email=validated_data["email"]
            )
            user.set_password(validated_data["password"])
            user.save()
            return user


class FootballFieldUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballField

    fields = ["bron", "date"]


class ProfileUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ("username", "email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        # Parolni shifrlash
        hashed_password = make_password(password)

        user = ProfileUser.objects.create(
            username=username,
            password=hashed_password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
