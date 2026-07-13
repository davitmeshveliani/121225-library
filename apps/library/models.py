import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Author(UUIDModel, TimeStampedModel):
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'))
    profile = models.URLField(blank=True, verbose_name=_('Profile URL'))
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_('Rating')
    )

    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Deleted at'))

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def __str__(self):
        return f'{self.first_name[0]}. {self.last_name}; {self.date_of_birth}'


class AuthorDetail(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name=_('Author')
    )

    biography = models.TextField(blank=True, verbose_name=_('Biography'))
    birth_city = models.CharField(blank=True, max_length=50, verbose_name=_('Birth City'))
    gender = models.CharField(choices=Gender.choices, max_length=1, verbose_name=_('Gender'))

    def __str__(self):
        return f'Details of {self.author}'




