from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response

from api_foodgram.serializers.users import (
    FollowSerializer,
    SubscribtionsSerializer)
from users.models import Follow

User = get_user_model()


class SubscribtionsListViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    serializer_class = SubscribtionsSerializer
    # queryset = User.objects.all()

    def get_queryset(self):
        subscriber = User.objects.get(
            pk=self.request.user.pk
        )
        follow_model = Follow.objects.filter(subscriber=subscriber)
        new_queryset = []
        for obj in follow_model:
            user = User.objects.get(
                pk=obj.user.pk
            )
            new_queryset.append(user)
        return new_queryset


class FollowAPIView(generics.CreateAPIView,
                    generics.DestroyAPIView):
    """Подписка/отписка на автора."""
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = self.request.user
        new_queryset = Follow.objects.filter(user=user)
        return new_queryset

    def perform_create(self, serializer):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        subscriber = self.request.user
        if serializer.is_valid():
            serializer.save(
                user=user,
                subscriber=subscriber)
            # output_serializer = SubscribtionsSerializer(
            #     user, context={'request': self.request}
            # )
            # return Response(
            #     output_serializer.data,
            #     status=status.HTTP_201_CREATED
            # )
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
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
