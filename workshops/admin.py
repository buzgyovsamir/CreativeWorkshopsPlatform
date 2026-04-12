from django.contrib import admin

from .models import Category, Tag, Workshop


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'organizer',
        'start_datetime',
        'status',
        'available_spots',
    )
    list_filter = ('status', 'category', 'city')
    search_fields = ('title', 'description', 'city')
    prepopulated_fields = {'slug': ('title',)}