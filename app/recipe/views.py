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
        is_assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        query_set = self.queryset
        if is_assigned_only:
            query_set = query_set.filter(recipe__isnull=False).distinct()
        return query_set.filter(user=self.request.user).order_by('-name')

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

    def _params_to_int_list(self, qs):
        """
        Helper funtion to parse query params to list of ints
        """
        return [int(q_id) for q_id in qs.split(',')]

    def get_queryset(self):
        query_set = self.queryset
        tags = self.request.query_params.get('tags')
        ingrediants = self.request.query_params.get('ingrediants')
        if tags:
            tag_ids = self._params_to_int_list(tags)
            query_set = query_set.filter(tags__id__in=tag_ids)
        if ingrediants:
            ing_ids = self._params_to_int_list(ingrediants)
            query_set = query_set.filter(ingrediants__id__in=ing_ids)

        return query_set.filter(user=self.request.user).order_by('-id')

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
