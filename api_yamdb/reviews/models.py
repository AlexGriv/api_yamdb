from django.db import models

from .validators import validate_year


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    year = models.IntegerField('Год издания', validators=[validate_year])

    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    genre = models.ManyToManyField(
        Genres,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
