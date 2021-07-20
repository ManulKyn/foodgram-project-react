from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, IngredientViewSet, PurchaseViewSet,
                    RecipeViewSet, SubscriptionViewSet, TagViewSet)

router = DefaultRouter()

router.register(
    r'purchases',
    PurchaseViewSet,
    basename='purchases'
)
router.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredients'
)
router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorites'
)
router.register(
    r'tags',
    TagViewSet,
    basename='tags'
)
router.register(
    r'users/subsciptions',
    SubscriptionViewSet,
    basename='subscription'
)
router.register(
    r'users/(?P<user_id>\d+)/subscripe',
    SubscriptionViewSet,
    basename='subscription'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
