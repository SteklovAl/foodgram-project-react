import io
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen.canvas import Canvas
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, Recipe,
                            RecipeIngredientDetails, ShoppingCart, Tag)

from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, ShoppingCartSerializer,
                          FavoriteSerializer)


class ListRetrieveCustomViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """GET запросы."""
    pass


class IngredientViewSet(ListRetrieveCustomViewSet):
    """
    Получение списка ингредиентов.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AuthorOrReadOnly,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка тэгов.
    """
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AuthorOrReadOnly]

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'GET':
            favorite_recipe, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = FavoriteSerializer()
                return Response(
                    serializer.to_representation(instance=favorite_recipe),
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
        methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'GET':
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
        canvas.setFont('Times-Roman', 36)
        canvas.drawString(70, 800, 'Продуктовый помощник')
        canvas.drawString(70, 760, 'список покупок:')
        canvas.setFont('Times-Roman', size=18)
        canvas.drawString(70, 700, 'Ингредиенты:')
        canvas.setFont('Times-Roman', size=16)
        canvas.drawString(70, 670, 'Название:')
        canvas.drawString(220, 670, 'Количество:')
        canvas.drawString(350, 670, 'Единица измерения:')
        height = 630
        for ingredient in ingredients:
            canvas.drawString(70, height, f"{ingredient['ingredient__name']}")
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
