from django.contrib import admin
from django.db.models import F
from django.db.models.functions import Round
from django.utils.html import format_html

from .models import (
                    Author,
                    AuthorDetail,
                    Category,
                    Library,
                    Member,
                    Book,
                    Posts
)



class AuthorDetailInline(admin.StackedInline):
    model = AuthorDetail


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'genre', 'page_count', 'category', 'author', 'visual_page_count')
    list_editable = ('title', 'author', 'genre', 'page_count', 'category')
    ordering = ('-title', 'author')
    search_fields = ('title', 'author')
    list_filter = ('category', 'genre')
    fields = ('title', 'author', 'genre', 'page_count', 'category', 'photo')
    list_per_page = 25


    @admin.action(description="Увеличить количество страниц на 10 %%")
    def increase_price_by_ten_percent(self, request, objects):
        objects.update(
            page_count=F('page_count') + 100
        )

    actions = [increase_price_by_ten_percent]

    @admin.display(description="Page Count")
    def visual_page_count(self, obj: Book):
        if obj.page_count < 100:
            color = "green"
        elif 100 <= obj.page_count < 300:
            color = "orange"
        else:
            color = "red"

        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.page_count
        )


class BookInline(admin.TabularInline):
    model = Book
    extra = 5


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [AuthorDetailInline, BookInline]

#
#
# admin.site.register(Posts)
# admin.site.register(Author)
# admin.site.register(AuthorDetail)
# admin.site.register(Category)
# admin.site.register(Member)
#
#
#
# @admin.register(Library)
# class LibraryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ["name"]}
#
