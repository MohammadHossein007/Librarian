from django.contrib import admin
from django.db.models.aggregates import Count
from . import models


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):   
    list_display = ['title', 'author', 'get_category', 'is_available', 'placed_at']
    search_fields = ['title', 'author']
    filter_horizontal = ['category',]
    list_select_related = ['author']

    def get_category(self, obj):
        return "|".join([c.title for c in obj.category.all()])
    

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'book_count']
    search_fields = ['title']
    ordering = ['title']

    @admin.display(ordering='book_count')
    def book_count(self, category):
        return category.book_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            book_count = Count('book')
        )


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'borrowed_on', 'return_by', 'status']
    search_fields = ['member', 'book', 'borrowed_on']
    list_filter = ['borrowed_on', 'return_by', 'status']


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(models.Member)
