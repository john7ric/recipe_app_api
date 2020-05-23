from rest_framework import serializers

from core.models import Tag, Ingrediant


class TagSerializer(serializers.ModelSerializer):
    """
    serializer class for tags
    """
    class Meta:
        model = Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class IngrediantSerializer(serializers.ModelSerializer):
    """
    serilaizer cla for Ingrediants
    """

    class Meta:
        model = Ingrediant
        fields = ('id', 'name',)
        read_only_fields = ('id',)
