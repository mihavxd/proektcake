from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            send_mail(subject='Заказ Ванилинка',
                      message='Сделан новый заказ на сайте Ванилинка',
                      from_email='vanil-lnka@yandex.ru',
                      recipient_list=['mihavxd@yandex.ru'],
                      fail_silently=True)
            html_content = render_to_string(
                "orders/order/mail_created.html",
                context={'order': order},
            )
            msg = EmailMultiAlternatives(
                "Заказ Ванилинка",
                html_content,
                "vanil-lnka@yandex.ru",
                [form.cleaned_data['email']],
                headers={"List-Unsubscribe": "<mailto:vanil-lnka@yandex.ru>"},
            )
            msg.attach_alternative(html_content,  "text/html")
            msg.send()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         post=item['post'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистить корзину
            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


