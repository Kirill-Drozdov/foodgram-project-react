from django.urls import include, path
from rest_framework import routers

from api_foodgram.views import recipes, users

app_name = 'api_foodgram'

router = routers.DefaultRouter()
router.register(
    'tags',
    recipes.TagViewSet,
    basename='tags'
)
router.register(
    'ingredients',
    recipes.IngredientViewSet,
    basename='ingredients'
)
router.register(
    'recipes',
    recipes.RecipeViewSet,
    basename='recipes'
)
router.register(
    'users/subscriptions',
    users.SubscriptionsListViewSet,
    basename='subscriptions'
)

urlpatterns = [
    path('recipes/download_shopping_cart/',
         recipes.download_shopping_cart,
         name='download_shopping_cart'
         ),
    path('', include(router.urls)),
    path('', include('djoser.urls.base')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/',
         users.FollowAPIView.as_view(),
         name='subscribe'),
    path('recipes/<int:pk>/favorite/',
         recipes.FavoriteAPIView.as_view(),
         name='favorite'),
    path('recipes/<int:pk>/shopping_cart/',
         recipes.ShoppingCartAPIView.as_view(),
         name='shopping_cart'),
]
