from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response

from api_foodgram.serializers.users import FollowSerializer
from users.models import Follow

User = get_user_model()


class CreateDeleteViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class FollowAPIView(generics.CreateAPIView,
                    generics.DestroyAPIView):
    """Подписка/отписка на автора."""
    serializer_class = FollowSerializer
    # filter_backends = (filters.SearchFilter,)
    # filterset_fields = ('following',)
    # search_fields = ('=following__username',)

    def get_queryset(self):
        user = self.request.user
        print(self.request)
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
