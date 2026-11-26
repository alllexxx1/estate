from decimal import Decimal

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Property(models.Model):
    TYPE_CHOICES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('room', 'Комната'),
    ]
    DEAL_CHOICES = [('rent', 'Аренда'), ('sale', 'Продажа')]


    owner: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name='Владелец'
    )
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    property_type = models.CharField('Тип объекта', max_length=10, choices=TYPE_CHOICES)
    deal_type = models.CharField('Тип сделки', max_length=10, choices=DEAL_CHOICES)
    city = models.CharField('Город', max_length=100)
    address = models.CharField('Адрес', max_length=200)
    rooms = models.PositiveSmallIntegerField('Количество комнат', validators=[MinValueValidator(1)])
    area = models.DecimalField(
        'Площадь, м2', max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal('2.00'))],
    )
    price = models.DecimalField(
        'Цена', max_digits=14, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Для аренды укажите цену за месяц, для продажи – полную стоимость',
    )
    photo = models.ImageField('Фотография', upload_to='properties/')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объект недвижимости'
        verbose_name_plural = 'Объекты недвижимости'

    def __str__(self) -> str:
        return self.title


class DealRequest(models.Model):
    property: Property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='deal_requests',
        verbose_name='Объект недвижимости'
    )
    applicant: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='deal_requests',
        verbose_name='Объект недвижимости'
    )
    phone = models.CharField('Телефон для связи', max_length=30)
    message = models.CharField('Сообщение', max_length=400)
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка на сделку'
        verbose_name_plural = 'Заявки на сделку'

    def __str__(self) -> str:
        return f'{self.applicant.username}: {self.property.title}'
