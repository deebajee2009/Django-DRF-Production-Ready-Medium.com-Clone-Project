"""
Profiles app views.
"""
# TODO: change this in production
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Prefetch

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from authors_api.settings.local import DEFAULT_FROM_EMAIL
from .exceptions import CantFollowYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import (
    ProfileJSONRenderer,
    ProfilesJSONRenderer,
)
from .serializers import (
    ProfileSerializer,
    UpdateProfileSerializer,
    FollowingSerializer,
)


User= get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    """
    Docstring for ProfileListAPIView
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = (ProfilesJSONRenderer,)

class ProfileDetailAPIView(generics.DestroyAPIView):
    """
    Docstring for ProfileDetailAPIView
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile

class UpdateProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    renderer_classes = [ProfileJSONRenderer]

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# Better approach
# class UpdateProfileAPIView(generics.RetrieveUpdateAPIView):
#     serializer_class = UpdateProfileSerializer
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, JSONParser]
#     renderer_classes = [ProfileJSONRenderer]

#     def get_object(self):
#         return self.request.user.profile


class FollowerListView(APIView):
    """
    Docstring for FollowerListView
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = (
                Profile.objects
                .select_related('user')
                .prefetch_related(
                    Prefetch(
                        'followers',
                        queryset=Profile.objects.select_related('user')
                    )
                )
                .get(user=request.user)
            )

            follower_profiles_list = list(profile.followers.all())
            serializer = FollowingSerializer(follower_profiles_list, many=True)

            formated_response = {
                "followers_count": len(follower_profiles_list),
                "followers": serializer.data
            }

            return Response(formated_response, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

class FollowingListView(APIView):
    """
    Docstring for FollowingListView
    """