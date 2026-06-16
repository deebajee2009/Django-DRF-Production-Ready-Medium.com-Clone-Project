"""
Response app views.
"""
from rest_framework import generics
from rest_framework.generics import get_object_or_404
# from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions

from .models import Article, Response
from .serializers import ResponseSerializer
from .permissions import IsResponseOwnerOrReadOnly


class ResponseListCreateView(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResponseSerializer

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Response.objects.filter(article__id=article_id,
                                       parent_response=None)

    def perform_create(self, serializer):
        user = self.request.user
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        serializer.save(user=user, article=article)


class ResponseUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated, IsResponseOwnerOrReadOnly]
    lookup_field = "id"

    # Because we used IsResponseOwnerOrReadOnly we do not use these anymore!
    # def perform_update(self, serializer):
    #     user = self.request.user
    #     response = self.get_object()
    #     if user != response.user:
    #         raise PermissionDenied("You do not have permission to update!")

    #     serializer.save()

    # def perform_destroy(self, instance):
    #     user = self.request.user
    #     response = self.get_object()
    #     if user != response.user:
    #         raise PermissionDenied(
    #             "You do not have to delete!"
    #         )

    #     instance.delete()
