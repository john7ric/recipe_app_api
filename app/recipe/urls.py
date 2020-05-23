from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagListViewSet, IngrediantViewSet

app_name = 'recipe'

router = DefaultRouter()
router.register('tag', TagListViewSet)
router.register('ingrediant', IngrediantViewSet)

urlpatterns = [
    path('', include(router.urls))
]
