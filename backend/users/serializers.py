from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers

from .models import Follow, User


class UserCreateSerializer(UserCreateSerializer):
    """Сериализация данных пользователя при регистрации."""
    email = serializers.EmailField(
        required=True,
    )
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )

    def validate_username(self, attrs):
        if User.objects.filter(username=attrs).exists():
            raise serializers.ValidationError(
                'Такой username уже зарегистрирован!'
            )
        return attrs

    def validate_email(self, attrs):
        if User.objects.filter(email=attrs).exists():
            raise serializers.ValidationError(
                'Такой email уже зарегистрирован!'
            )
        return attrs


class CustomUserSerializers(UserSerializer):
    """
    Сереализация пользователей с дополнительным полем is_subscribed.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class FollowRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализация рецептов для FollowSerializer.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes.count', read_only=True
    )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return FollowRecipeSerializer(queryset, many=True).data

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
