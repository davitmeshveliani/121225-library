"""
Management command: seed_books

Generates fake data for Book and Author.

Usage:
    python manage.py seed_books
    python manage.py seed_books --books 30 --authors 8
    python manage.py seed_books --flush

Requires Faker:
    pip install Faker
"""

import random

from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from faker import Faker

from apps.library.models import Author, Book


fake = Faker()


class Command(BaseCommand):
    help = (
        "Generates fake Book and Author records using Faker. "
        "Use --authors and --books to control how many records are created. "
        "Use --flush to delete all existing Book and Author records before generating new ones."
    )

    def add_arguments(self, parser):
        parser.add_argument("--authors", type=int, default=8, help="Number of authors to create")
        parser.add_argument("--books", type=int, default=30, help="Number of books to create")
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing Book and Author records before generating new ones",
        )

    def handle(self, *args, **options):
        n_authors = options["authors"]
        n_books = options["books"]

        if options["flush"]:
            self.stdout.write(self.style.WARNING("Deleting existing data..."))
            Book.objects.all().delete()
            Author.objects.all().delete()

        with transaction.atomic():
            authors = self._create_authors(n_authors)
            books = self._create_books(n_books, authors)

        self.stdout.write(self.style.SUCCESS(
            f"Done: created {len(authors)} authors and {len(books)} books."
        ))

    def _create_authors(self, count):
        authors = []
        for _ in range(count):
            author = Author.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=90),
                profile=fake.url(),
                rating=fake.random_int(min=1, max=10),
            )
            authors.append(author)
        return authors

    def _create_books(self, count, authors):
        books = []
        max_attempts_per_book = 20
        skipped = 0

        for _ in range(count):
            book = None
            for _attempt in range(max_attempts_per_book):
                try:
                    with transaction.atomic():
                        book = Book.objects.create(
                            title=fake.sentence(nb_words=4).rstrip("."),
                            author=random.choice(authors) if authors else None,
                            published_at=fake.date_between(start_date="-40y", end_date="today"),
                            genre=random.choice(Book.Genre.values),
                            page_count=fake.random_int(min=50, max=900),
                            description=fake.paragraph(nb_sentences=5),
                        )
                    break
                except IntegrityError:
                    continue

            if book is None:
                skipped += 1
                continue

            books.append(book)

        if skipped:
            self.stdout.write(self.style.WARNING(
                f"Skipped {skipped} book(s) after {max_attempts_per_book} failed attempts "
                f"each (unique_together collisions on author/title or author/published_at). "
                f"Consider increasing --authors."
            ))

        return books