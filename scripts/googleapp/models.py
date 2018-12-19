# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class AndroidVersion(models.Model):
    android_version_id = models.AutoField(primary_key=True)
    android_version = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'android_version'
        ordering = ['android_version']
        verbose_name = 'Android Version'
        verbose_name_plural = 'Android Version'

    def __str__(self):
        return self.android_version
    


class App(models.Model):
    app_id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=255)
    rating = models.CharField(max_length=10, blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    install = models.CharField(max_length=20, blank=True, null=True)
    price = models.CharField(max_length=10, blank=True, null=True)
    updated_time = models.CharField(max_length=20, blank=True, null=True)
    current_version = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    pay_type = models.ForeignKey('PayType', on_delete=models.CASCADE, blank=True, null=True)
    content_rating = models.ForeignKey('ContentRating', on_delete=models.CASCADE, blank=True, null=True)
    android_version = models.ForeignKey(AndroidVersion, on_delete=models.CASCADE, blank=True, null=True)

    # m2m
    genre = models.ManyToManyField('Genre', through='AppGenre')

    class Meta:
        managed = False
        db_table = 'app'
        ordering = ['app_name']
        verbose_name = 'App'
        verbose_name_plural = 'App'

    def __str__(self):
        return self.app_name


    def get_absolute_url(self):
        return reverse('app_detail', kwargs={'pk': self.pk})

    def genre_display(self):
            return ', '.join(
            genre.genre_name for genre in self.genre.all()[:5])

    genre_display.short_description = 'Genre'


    @property
    def genres(self):
        """
        Returns a list of genres.
        :return: string
        """
        genres = self.genre.order_by('genre_name')

        names = []
        for genre in genres:
            name = genre.genre_name
            if name is None:
                continue         
            if name not in names:
                names.append(name)

        return ', '.join(names)


class AppGenre(models.Model):
    app_genre_id = models.AutoField(primary_key=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'app_genre'
        ordering = ['app','genre']
        verbose_name = 'App Genre Relation'
        verbose_name_plural = 'App Genre Relation'

    


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'category'
        ordering = ['category_name']
        verbose_name = 'Category Name'
        verbose_name_plural = 'Category Name'

    def __str__(self):
        return self.category_name


class ContentRating(models.Model):
    content_rating_id = models.AutoField(primary_key=True)
    content_rating = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'content_rating'
        ordering = ['content_rating']
        verbose_name = 'Content Rating'
        verbose_name_plural = 'Content Rating'

    def __str__(self):
        return self.content_rating


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'genre'
        ordering = ['genre_name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genre'

    def __str__(self):
        return self.genre_name


class PayType(models.Model):
    pay_type_id = models.AutoField(primary_key=True)
    pay_type_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'pay_type'
        ordering = ['pay_type_name']
        verbose_name = 'Pay Type'
        verbose_name_plural = 'Pay Type'

    def __str__(self):
        return self.pay_type_name
