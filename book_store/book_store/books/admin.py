from django.contrib import admin

from .models import (
    Book,
    BookRentHistory,
    Category,
    InBoxMessages)
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    fields = ('category', )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'image', 'description', 'book_amount',
              'publish_date', 'number_of_pages', 'category')

    list_display = ('title', 'author', 'category', 'book_amount')
    search_fields = ['title']


@admin.register(BookRentHistory)
class BookRentHistoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rent_date')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(InBoxMessages)
class InBoxMessagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
