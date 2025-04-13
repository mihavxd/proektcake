from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # для автоматического формрования слага
    form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'price', 'available', 'get_photo', 'created_at', 'updated', 'views', 'new', 'sale', 'sale_price')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ['price', 'available', 'new', 'sale', 'sale_price']
    list_filter = ('category', 'tags', 'available', 'created_at', 'updated')
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ('title', 'slug', 'category', 'tags', 'content', 'photo',  'photo1', 'photo2', 'get_photo', 'views',
              'created_at', 'price', 'available', 'new', 'sale', 'sale_price')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # для автоматического формрования слага


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # для автоматического формрования слага


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name',  'post', 'rating', 'email', 'created_on', 'active', 'body',)
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)



admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
