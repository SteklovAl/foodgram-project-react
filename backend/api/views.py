import io

import reportlab
from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe,
                            RecipeIngredientDetails, ShoppingCart, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import LimitPagePagination
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка ингредиентов.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    search_fields = ('^name',)
    filter_class = IngredientSearchFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка тэгов.
    """
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Получение списка рецептов.
    Получение рецепта.
    Создание, обновление, удаление рецепта.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filter_class = RecipeFilter
    pagination_class = LimitPagePagination

    @staticmethod
    def create_object(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            favorite_recipe, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = FavoriteSerializer()
                return Response(
                    serializer.to_representation(instance=favorite_recipe),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже добавлен в избранное'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            recipe, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = ShoppingCartSerializer()
                return Response(
                    serializer.to_representation(instance=recipe),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в корзине покупок'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredientDetails.objects.filter(
            recipe__shopping_carts__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit').order_by(
                    'ingredient__name').annotate(amount=Sum('amount'))
        buffer = io.BytesIO()
        canvas = Canvas(buffer)
        reportlab.rl_config.TTFSearchPath.append(
            str(settings.BASE_DIR) + '/backend')
        pdfmetrics.registerFont(
            TTFont('arial', 'arial.ttf', 'UTF-8'))
        canvas.setFont('arial', 32)
        canvas.drawString(60, 790, 'Продуктовый помощник')
        canvas.drawString(60, 750, 'список покупок:')
        canvas.setFont('arial', size=18)
        canvas.drawString(60, 690, 'Ингредиенты:')
        canvas.setFont('arial', size=16)
        canvas.drawString(60, 660, 'Название:')
        canvas.drawString(220, 660, 'Количество:')
        canvas.drawString(350, 660, 'Единица измерения:')
        height = 620
        for ingredient in ingredients:
            canvas.drawString(60, height, f"{ingredient['ingredient__name']}")
            canvas.drawString(250, height,
                              f"{ingredient['amount']}")
            canvas.drawString(380, height,
                              f"{ingredient['ingredient__measurement_unit']}")
            height -= 25
        canvas.showPage()
        canvas.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='shopping_cart.pdf')
