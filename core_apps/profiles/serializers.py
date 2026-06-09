"""
Profiles app serializers.
"""
from rest_framework import serializers

from django_countries.serializer_fields import CountryField

from .models import Profile


class ProfileSerializer(serializers.SerializerMethodField):
    """
    Docstring for ProfileSerializer
    """
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "profile_photo",
            "phone_number",
            "full_name",
            "gender",
            "country",
            "city",
            "twitter_handle",
            "about_me"
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Docstring for UpdateProfileSerializer
    """
    coountry = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "twitter_handle"
        ]

class FollowingSerializer(serializers.ModelSerializer):
    """
    Docstring for FollowingSerializer
    """
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile