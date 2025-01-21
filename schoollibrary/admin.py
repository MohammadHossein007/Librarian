from django.contrib import admin
from django.db.models import Q
from django.db.models.aggregates import Count
from . import models
admin.site.site_title = 'پنل مدیریت'
admin.site.site_header = 'پنل مدیریت'

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'get_category', 'is_available', 'jplaced_at']
    search_fields = ['title', 'author__name']
    filter_horizontal = ['category', ]
    list_select_related = ['author']

    def get_category(self, obj):
        return " | ".join([c.title for c in obj.category.all()])
    get_category.short_description='دسته بندی ها'


class BookCountFilter(admin.SimpleListFilter):
    title = 'تعداد کتاب'
    parameter_name = 'تعداد کتاب'

    def lookups(self, request, model_admin):
        return (
            ('>10', 'بیشتر از 10'),
            ('<=10', 'کمتر از 10'),
        )

    def queryset(self, request, queryset):
        if self.value() == '>10':
            return queryset.filter(book_count__gt=10)
        if self.value() == '<=10':
            return queryset.filter(book_count__lte=10)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'book_count']
    search_fields = ['title']
    ordering = ['title']
    list_filter = [BookCountFilter]

    @admin.display(ordering='book_count')
    def book_count(self, category):
        return category.book_count

    book_count.short_description = 'تعداد کتاب ها'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            book_count=Count('book')
        )


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'jborrowed_on', 'jreturn_by', 'status']
    search_fields = ['member__first_name', 'book__title', 'borrowed_on']
    list_filter = ['borrowed_on', 'return_by', 'status']


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'membership_id', 'jmembership_start_date',
                    'jmembership_end_date', 'is_active', 'borrowed_books']
    search_fields = ['membership_id', 'first_name', 'last_name']
    list_filter = ['membership_start_date', 'membership_end_date', 'is_active']

    def borrowed_books(self, obj):
        loans = models.Loan.objects.filter(
            Q(member=obj) & (Q(status='borrowed') | Q(status='overdue'))
        )
        books = [loan.book.title for loan in loans]
        if books:
            return ", ".join(books)  # Return book titles as a comma-separated string
        return "هیچ کتابی قرض گرقته نشده"

    borrowed_books.short_description = 'کتاب های قرض گرفته شده'
