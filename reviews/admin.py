from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'workshop', 'rating', 'is_visible', 'created_at')
    list_filter = ('rating', 'is_visible', 'created_at')
    search_fields = ('author__username', 'workshop__title', 'comment')