import os
import sys
import django
from timeit import timeit

from django.utils.text import slugify
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.library.models import Book, Author, Library


def create_library():
    obj = Library.objects.create(
        name='City Library',
        location='New York, NY, USA',
        site='https://city.city-library.com',
        slug='city-library',
    )
    print(obj.id)
    print(obj)
    print(type(obj))


def create_library_1():
    obj = Library(
        name='Country Library',
        location='Berlin',
        site='https://city.city-library.com'
    )
    print(obj.id)
    print(obj)
    print(type(obj))
    obj.save()


def get_all():
    libraries = Library.objects.all()
    print(libraries)

    print(list(libraries))

    # print(type(libraries))
    #
    # for item in libraries:
    #     print(item)
    #     print(type(item))

    # print(sys.getsizeof(libraries))
    # print(sys.getsizeof(list(libraries)))



def update_library():
    obj = Library.objects.get(id='bb5bdb6f-4057-43bb-a803-a46b58ac698c')
    obj.name = 'District Main Library'
    obj.save()


def get_objects():
    libraries_all = Library.objects.all() # SELECT * FROM libraries
    print(libraries_all)

    first_library = Library.objects.first() # смотри в orderibg
    print(first_library)

    first_library = Book.objects.first() # если 0 записей - None
    print(first_library)

    first_library = Book.objects.all() # если 0 записей - QuerySet[]
    print(first_library)

    last_library = Library.objects.last()
    print(last_library)

    # Замер времени выполнения
    number_library = Book.objects.all().count() # SELECT COUNT(*) FROM books
    print(number_library)

    # Замер времени выполнения
    number_library = len(Book.objects.all())
    print(number_library)

    number_library = Book.objects.all().exists()
    print(number_library)

    values = Library.objects.all().values('name', 'slug') # SELECT name, slug from libraries
    print(values)

def filter_books():
    libraries_all = Library.objects.filter(name='Country Library', location='Berlin')
    print(libraries_all)

    libraries_all = Library.objects.filter(name='Country Library').filter(location='Berlin')
    print(libraries_all)


def filter_books_by_pages():
    books = Book.objects.filter(page_count__lt=200)
    for book in books:
        print(book, book.page_count)


def filter_with_Q_1():
    books = Book.objects.filter(page_count__lt=55, genre=Book.Genre.HORROR)
    for book in books:
        print(book, book.genre)

    print('-' * 100)

    books = Book.objects.filter(page_count__lt=55).filter(genre=Book.Genre.HORROR)
    for book in books:
        print(book, book.genre)

    print('-' * 100)

    books = Book.objects.filter(Q(page_count__lt=55) & Q(genre=Book.Genre.HORROR))
    for book in books:
        print(book, book.genre)


def filter_with_Q_2():
    books = Book.objects.filter(Q(genre=Book.Genre.HORROR) | Q(genre=Book.Genre.FICTION) | Q(page_count__lt=55))

    for book in books:
        print(book, book.genre)



def filter_with_Q_2_updare():
    # books = (Book.objects.filter(Q(genre=Book.Genre.HORROR) | Q(genre=Book.Genre.FICTION) | Q(page_count__lt=55))
    #          .update(description='trulala'))
    #
    # print(books)

    books = (Book.objects.filter(Q(genre=Book.Genre.HORROR) | Q(genre=Book.Genre.FICTION) | Q(page_count__lt=55)))

    for book in books:
        print(book, book.description)



def filter_with_F():
    books = (Book.objects.filter(Q(genre=Book.Genre.HORROR) | Q(genre=Book.Genre.FICTION) | Q(page_count__lt=55))
             .update(description='description[:3].upper()'))

    print(books)

    books = (Book.objects.filter(Q(genre=Book.Genre.HORROR) | Q(genre=Book.Genre.FICTION) | Q(page_count__lt=55)))

    for book in books:
        print(book, book.description)



if __name__ == '__main__':
    filter_with_Q_2_updare()