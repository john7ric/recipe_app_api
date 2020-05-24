from rest_framework import serializers

from core.models import Tag, Ingrediant, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer class for managign recipe models
    """
    ingrediants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingrediant.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'time_minutes', 'price',
            'link', 'ingrediants', 'tags'
            )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """
    Serializer for recipe detail (retrieve) action
    """
    ingrediants = IngrediantSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
