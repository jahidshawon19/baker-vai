from django.contrib import admin
from .models import Category, Essay, EssayQuote


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class EssayQuoteInline(admin.TabularInline):
    model = EssayQuote
    extra = 1


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'featured', 'created_at')
    list_filter = ('status', 'featured', 'category')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [EssayQuoteInline]
    fieldsets = (
        (None, {'fields': ('title', 'category')}),
        ('Content', {'fields': ('content',)}),
        ('Publishing', {'fields': ('status', 'featured', 'published_at', 'created_by')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(EssayQuote)
class EssayQuoteAdmin(admin.ModelAdmin):
    list_display = ('essay', 'quote')
    search_fields = ('quote', 'essay__title')
