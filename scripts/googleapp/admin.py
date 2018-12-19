from django.contrib import admin
import googleapp.models as models
# Register your models here.


@admin.register(models.AndroidVersion)
class AndroidVersionAdmin(admin.ModelAdmin):
	fields = ['android_version']
	list_display = ['android_version']
	ordering = ['android_version']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
	fields = ['category_name']
	list_display = ['category_name']
	ordering = ['category_name']

@admin.register(models.ContentRating)
class ContentRatingAdmin(admin.ModelAdmin):
	fields = ['content_rating']
	list_display = ['content_rating']
	ordering = ['content_rating']

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
	fields = ['genre_name']
	list_display = ['genre_name']
	ordering = ['genre_name']

@admin.register(models.PayType)
class PayTypeAdmin(admin.ModelAdmin):
	fields = ['pay_type_name']
	list_display = ['pay_type_name']
	ordering = ['pay_type_name']

@admin.register(models.App)
class AppAdmin(admin.ModelAdmin):
    fields = ['app_name','rating','reviews','size','install','price','updated_time','current_version','category','pay_type','content_rating','android_version']
    list_display = ['app_name','rating','reviews','size','install','price','updated_time','current_version','category','pay_type','content_rating','android_version','genre_display']
    ordering = ['app_name','updated_time']
    list_filter = ['app_name']

    
	

