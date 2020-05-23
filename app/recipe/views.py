from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Tag, Ingrediant
from recipe.serializers import TagSerializer, IngrediantSerializer


class TagListViewSet(viewsets.ModelViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin):
    """
    Viewset for listing the tags
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IngrediantViewSet(viewsets.ModelViewSet, mixins.ListModelMixin):
    """
    View set for managing Ingrediants
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = IngrediantSerializer
    queryset = Ingrediant.objects.all()

    def get_queryset(self):
        queryset = Ingrediant.objects.filter(
            user=self.request.user).order_by('-name')
        return queryset
