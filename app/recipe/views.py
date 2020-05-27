from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Tag, Ingrediant, Recipe
from recipe.serializers import (
    TagSerializer, IngrediantSerializer, RecipeSerializer,
    RecipeDetailSerializer, RecipeImageSerializer
)


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


class RecipeViewSet(viewsets.ModelViewSet):
    """
    View Set for Recipe models
    """
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer
        else:
            return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """
        Custom Viewset action for uploading and image
        """
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
