from django.db import models
from django.urls import reverse
from users.models import User

# Create your models here.


class Ticket(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name='Наименование'
    )
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField('Цена', decimal_places=2, max_digits=5)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Талон для добавления к продажам'
        verbose_name_plural = 'Варианты талонов на продажу'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'ticket_detail',
            kwargs={
                'ticket_slug': self.slug,
            }
        )


class Order(models.Model):
    customer = models.ForeignKey(User, related_name='customer',
                                 on_delete=models.CASCADE, verbose_name='Покупатель')
    tickets = models.ManyToManyField(
        Ticket, verbose_name='Талоны', blank=True, through='TicketsInOrder')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время создания')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.customer} - {self.created.day}/{self.created.month}/{self.created.year}'


class TicketsInOrder(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='Заказ')
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT,
                                verbose_name='Товар', related_name='count_in_order',)
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара в заказе')

    class Meta:
        verbose_name = 'Все заказы'
        verbose_name_plural = 'История заказов'
    
    def __str__(self):
        return f'{self.order} - {self.ticket.title}, {self.quantity} шт'