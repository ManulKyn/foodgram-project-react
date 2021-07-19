import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    dimension = models.CharField(max_length=128, verbose_name='ед. измерения')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Инргедиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.title} {self.dimension}'


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
        max_length=200,
        verbose_name='Стиль'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    title = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='templates/media/',
        blank=True,
        verbose_name='Картинка',
        help_text='Загрузите изображение'
    )
    text = models.TextField(
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
        verbose_name='Тег'
    )
    time = models.PositiveIntegerField(
        verbose_name='Время приготовления (мин)',
        validators=[MinValueValidator(1)]
    )
    slug = models.SlugField(unique=True, max_length=256, default=uuid.uuid1,)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'{self.title} от {self.author}'

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'slug': self.slug})


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
