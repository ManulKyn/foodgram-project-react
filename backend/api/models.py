import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import format_html
from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название',
    )
    dimension = models.CharField(max_length=128, verbose_name='ед. измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Инргедиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name} {self.dimension}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Тег'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Слаг',
        default=uuid.uuid1
    )
    style = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name='Стиль/Цвет'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.hex_color,
        )


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes',
        blank=True,
        verbose_name='Картинка',
        help_text='Загрузите изображение'
    )
    text = models.TextField(
        max_length=256,
        verbose_name='Текстовое описание',
        default='Еще нет описания'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        verbose_name='Тег',
    )
    time = models.PositiveIntegerField(
        verbose_name='Время приготовления (мин)',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'{self.title} от {self.author}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_recipes'
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self) -> str:
        return (f'{self.ingredient.title} {self.amount} '
                f'{self.ingredient.dimension} в {self.recipe}'
                )


class Favorite(models.Model):
    """
    Stores a favorite relation between `auth.User` and `recipes.Recipe`.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favored_by',
        verbose_name='Рецепт в избранном',
    )
    when_added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe'
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Subscription(models.Model):
    """
    Stores a subscription relation between two `auth.User`.
    User is subscribed to author.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписался на',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} => {self.author}'


class Purchase(models.Model):
    """
    Stores a purchase relation between `auth.User` and `recipes.Recipe`.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в покупках',
    )
    when_added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase'
            )
        ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
