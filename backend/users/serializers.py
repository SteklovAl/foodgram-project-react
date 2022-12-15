from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe

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
            'password',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class FollowRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализация рецептов для FollowListSerializer.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes.count', read_only=True
    )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.objects.filter(
            author=obj, user=self.context['request'].user
        ).exists()

    def get_recipes(self, obj):
        request = self.context['request']
        limit = request.GET.get('recipes_limit')
        author = get_object_or_404(User, id=obj.pk)
        recipes = author.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = FollowRecipeSerializer(
            recipes,
            many=True,
            context={'request': request}
        )
        return serializer.data

    class Meta:
        model = User
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


class FollowCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=CurrentUserDefault(),
        ),
    author = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all())

    def validate(self, data):
        user = data['user']
        author = data['author']
        if self.context['request'].method == 'POST' and user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на данного автора'
            )
        ]
