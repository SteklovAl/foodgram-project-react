from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# UNIT = [
#     ('л', 'литры'),
#     ('г', 'граммы'),
#     ('ст. л', 'столовая ложка'),
#     ('ч. л', 'чайная ложка'),
#     ('ст. л', 'столовая ложка'),
#     ]


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        blank=False,
        max_length=200,
        verbose_name='Название'
    )
    color = ColorField('Цвет HEX', unique=True)

    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name='Слаг'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-name']


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-name']


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        blank=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientDetails'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='тэг',
        help_text='Выберите тэг'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления'
    )

    def __str__(self) -> str:
        # выводим описание рецепта
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']


class RecipeIngredientDetails(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amount')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amount')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
    )


class Favorite(models.Model):
    """
    Избранные рецепты
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name="favorites",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'избранное пользователя {self.user}'

    class Meta():
        ordering = ['-id']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    """
    Список покупок
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Рецепт'
        )

    def __str__(self):
        return f'список покупок пользователя {self.user}'

    class Meta():
        ordering = ['-id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_recording')
