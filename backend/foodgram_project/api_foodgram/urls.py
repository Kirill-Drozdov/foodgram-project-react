from django.urls import include, path
from rest_framework import routers

from api_foodgram.views import recipes

app_name = 'api_foodgram'

router = routers.DefaultRouter()
router.register('tags', recipes.TagViewSet, basename='tags')
router.register(
    'ingredients',
    recipes.IngredientViewSet,
    basename='ingredients'
)
# router.register('users', users.UserViewSet, basename='users')

urlpatterns = [
    # path('v1/auth/signup/', SignUpViewSet.as_view()),
    # path('v1/auth/token/', TokenViewSet.as_view()),
    # path('', include('djoser.urls')),
    # path('', include('djoser.urls.jwt')),
    # path(r'auth/', include('djoser.urls')),
    path('', include("djoser.urls.base")),
    path('', include("djoser.urls.authtoken")),
    path('', include(router.urls)),
]
