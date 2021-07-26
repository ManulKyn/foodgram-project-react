# Generated by Django 3.2 on 2021-07-26 18:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',), 'verbose_name': 'Инргедиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='title',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='slug',
        ),
        migrations.AddField(
            model_name='favorite',
            name='when_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 7, 26, 18, 51, 27, 784715, tzinfo=utc), verbose_name='Дата добавления'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='name',
            field=models.CharField(default=datetime.datetime(2021, 7, 26, 18, 51, 57, 382498, tzinfo=utc), max_length=256, unique=True, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='when_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата добавления'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, help_text='Загрузите изображение', upload_to='recipes', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='api.Tag', verbose_name='Тег'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(default='Еще нет описания', max_length=256, verbose_name='Текстовое описание'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='style',
            field=models.CharField(default='#ffffff', max_length=7, verbose_name='Стиль/Цвет'),
        ),
    ]
