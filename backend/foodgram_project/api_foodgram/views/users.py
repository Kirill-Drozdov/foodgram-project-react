from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response

from api_foodgram.serializers.users import (
    FollowSerializer,
    SubscriptionsSerializer)
from users.models import Follow

User = get_user_model()


class SubscriptionsListViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        return User.objects.filter(
            followers__subscriber=self.request.user
        )


class FollowAPIView(generics.CreateAPIView,
                    generics.DestroyAPIView):
    """Подписка/отписка на автора."""
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        user = get_object_or_404(
            User,
            pk=self.kwargs.get('pk')
        )
        subscriber = self.request.user
        if serializer.is_valid():
            serializer.save(
                user=user,
                subscriber=subscriber)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(
            User,
            pk=self.kwargs.get('pk')
        )
        subscriber = get_object_or_404(
            User, username=self.request.user.username
        )
        instance = get_object_or_404(
            Follow,
            user=user,
            subscriber=subscriber
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
