from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagListViewSet, IngrediantViewSet, RecipeViewSet

app_name = 'recipe'

router = DefaultRouter()
router.register('tag', TagListViewSet)
router.register('ingrediant', IngrediantViewSet)
router.register('recipe', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
