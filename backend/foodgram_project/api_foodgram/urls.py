from django.urls import include, path
from rest_framework import routers

from api_foodgram.views import recipes, users

app_name = 'api_foodgram'

router = routers.DefaultRouter()
router.register('tags', recipes.TagViewSet, basename='tags')
router.register('users', users.UserViewSet, basename='users')

urlpatterns = [
    # path('v1/auth/signup/', SignUpViewSet.as_view()),
    # path('v1/auth/token/', TokenViewSet.as_view()),
    path('', include(router.urls)),
]
