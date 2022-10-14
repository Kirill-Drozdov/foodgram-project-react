# from django.shortcuts import get_object_or_404
from rest_framework import viewsets
# from rest_framework.response import Response

from recipes.models import Tag
from api_foodgram.serializers.recipes import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
