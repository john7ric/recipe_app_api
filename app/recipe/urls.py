from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagListViewSet

app_name = 'recipe'

router = DefaultRouter()
router.register('tag', TagListViewSet)

urlpatterns = [
    path('', include(router.urls))
]
