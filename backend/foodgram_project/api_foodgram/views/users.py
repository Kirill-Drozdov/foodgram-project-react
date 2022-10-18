from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

from api_foodgram.serializers.users import FollowSerializer
from foodgram_project.users.models import Follow

User = get_user_model()


class CreateDeleteViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class FollowViewSet(CreateDeleteViewSet):
    """Подписка/отписка на автора."""
    serializer_class = FollowSerializer
    # filter_backends = (filters.SearchFilter,)
    # filterset_fields = ('following',)
    # search_fields = ('=following__username',)

    def get_queryset(self):
        user = self.request.user
        new_queryset = Follow.objects.filter(user=user)
        return new_queryset

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        subscriber = get_object_or_404(User, pk=user_id)
        user = self.request.user
        if serializer.is_valid():
            serializer.save(
                user=user,
                subscriber=subscriber)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
