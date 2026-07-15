from django.contrib import admin

from .models import (
                    Author,
                    AuthorDetail,
                    Category,
                    Library,
                    Member,
                    Book,
                    Posts
)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'genre', 'page_count', 'category', 'author',)
    list_editable = ('title', 'author', 'genre', 'page_count', 'category')
    ordering = ('-title', 'author')
    search_fields = ('title', 'author')
    list_filter = ('category', 'genre')
    fields = ('title', 'author', 'genre', 'page_count', 'category')
    list_per_page = 25


admin.site.register(Posts)
admin.site.register(Author)
admin.site.register(AuthorDetail)
admin.site.register(Category)
admin.site.register(Member)



@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

