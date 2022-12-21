import io

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe,
                            RecipeIngredientDetails, ShoppingCart, Tag)
from reportlab.pdfgen.canvas import Canvas
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import LimitPagePagination
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


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
    permission_classes = (AllowAny,)
    search_fields = ('name',)
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

    # @staticmethod
    # def delete_object(request, pk, model):
    #     user = request.user
    #     recipe = get_object_or_404(Recipe, pk=pk)
    #     object = get_object_or_404(model, user=user, recipe=recipe)
    #     object.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def _create_or_destroy(self, http_method, recipe, key,
    #                        model, serializer):
    #     if http_method == 'POST':
    #         return self.create_object(request=recipe, pk=key,
    #                                   serializers=serializer)
    #     return self.delete_object(request=recipe, pk=key, model=model)

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
