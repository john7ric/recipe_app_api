from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Tag, Ingrediant
from recipe.serializers import TagSerializer, IngrediantSerializer


class BaseRecipeAttrViewSet(viewsets.ModelViewSet,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin):
    """
    Base class for user owned recipe attributes
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TagListViewSet(BaseRecipeAttrViewSet):
    """
    Viewset for listing the tags
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngrediantViewSet(BaseRecipeAttrViewSet):
    """
    View set for managing Ingrediants
    """
    serializer_class = IngrediantSerializer
    queryset = Ingrediant.objects.all()
