"""
Profiles app views.
"""
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Prefetch

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

# TODO: change this in production
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


User = get_user_model()


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
                .prefetch_related(
                    Prefetch(
                        'followers',
                        queryset=Profile.objects.select_related('user')
                    )
                )
                .get(user=request.user)
            )

            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)

            formated_response = {
                "followers_count": follower_profiles.count(),
                "followers": serializer.data
            }

            return Response(formated_response, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


class FollowingListView(APIView):
    """
    Docstring for FollowingListView
    """
    def get(self, request, user_id, format=None):
        try:
            profile = (
                Profile.objects
                .prefetch_related(
                    Prefetch(
                        'following',
                        queryset=Profile.objects.select_related('user')
                    )
                )
                .get(user__id=user_id)
            )

            following_profiles = profile.following.all()
            serializer = FollowingSerializer(following_profiles, many=True)

            formated_response = {
                "following_count": following_profiles.count(),
                "users_i_follow": serializer.data
            }

            return Response(formated_response, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


class FollowAPIView(APIView):
    """
    Handling following and add to follow of a profile account
    """
    def post(self, request, user_id, format=None):
        try:
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id = user_id)

            if profile == follower:
                raise CantFollowYourself()

            if user_profile.check_following(profile):
                formated_response = {
                    "message": f"You are already following {profile.user.first_name} {profile.user.last_name}",
                }
                return Response(formated_response, status=status.HTTP_400_BAD_REQUEST)

            user_profile.follow(profile)
            subject = "A new user follows you"
            message = f"Hi there, {profile.user.first_name}!!, the user \
            {user_profile.user.first_name} {user_profile.user.last_name} now \
            follows you "
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [profile.user.email]
            send_mail(subject, message, from_email, recipient_list,
                      fail_silently=True)

            return Response(
                {
                    "message": f"You are now following {profile.user.first_name} {profile.user.last_name}",
                },
                status=status.HTTP_200_OK
            )
        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that does not exist.")


class UnfollowAPIView(APIView):
    """
    Handling unfollow of a profile account.
    """
    def post(self, request, user_id, *args, **kwargs):
        user_profile = request.user.profile
        profile = Profile.objects.get(user__id=user_id)

        if not user_profile.check_following(profile)
            formatted_response = {
                "message": f"You can't unfollow {profile.user.first_name} \
                {profile.user.last_name}, since you were not following"
            }
            return Response(
                formatted_response,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_profile.unfollow(profile)

        formatted_response = {
                "message": f"You have unfollowed {profile.user.first_name} \
                {profile.user.last_name}, since you were not following"
            }
        return Response(
            formatted_response,
            status=status.HTTP_204_NO_CONTENT
        )
