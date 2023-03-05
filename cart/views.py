
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.models import Profile

from users.models import User
from cart.models import Order, TicketsInOrder
from main.models import TicketStore, TicketForProf
from uuid import uuid4


def add_to_cart(request):
    path = request.GET.get('next')

    if request.method == 'POST':
        ticket_id = request.GET.get('ticket_id')

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session.get('cart')
        if ticket_id in cart:
            cart[ticket_id]['quantity'] += 1

        else:
            cart[ticket_id] = {
                'quantity': 1
            }

    request.session.modified = True
    return redirect(path)


def view_cart(request):

    path = request.GET.get('next')

    context = {
        'next': path,
    }

    cart = request.session.get('cart', None)

    if cart:
        amount = 0.0
        tickets = {}
        ticket_list = TicketStore.objects.filter(pk__in=cart.keys()).values('id')
        for ticket in ticket_list:
            ticket['title'] = TicketStore.objects.filter(pk=ticket['id'])[0].ticket.title
            ticket['description'] = TicketStore.objects.filter(pk=ticket['id'])[0].ticket.description
            ticket['price'] = TicketStore.objects.filter(pk=ticket['id'])[0].ticket.price
            tickets[str(ticket['id'])] = ticket

        for key in cart.keys():
            cart[key]['ticket'] = tickets[key]
            amount += float(TicketStore.objects.filter(pk=key)[0].ticket.price) * cart[key]['quantity']

        context['cart'] = cart
        context['amount'] = amount


    return render(request, 'cart.html', context)


@login_required(login_url='login')
def view_order(request):
    if request.method == 'POST':
        user_id = request.user.pk
        customer = User.objects.get(pk=user_id)

        cart = request.session['cart']

        if len(cart) > 0:
            order = Order.objects.create(customer=customer)

            for key, value in cart.items():
                ticket = TicketStore.objects.get(pk=key)
                quantity = value['quantity']
                # Profile.objects.update(ticket=ticket.ticket)
                for i in range(1, quantity+1):
                    TicketForProf.objects.create(user_id=customer, title=ticket.ticket.title,
                        description = ticket.ticket.description, price = ticket.ticket.price, id_for_use = uuid4())
                TicketsInOrder.objects.create(order=order, ticket=ticket.ticket, quantity=quantity)

            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, 'Заказ принят')

    return redirect('cart:cart')
