from decimal import Decimal
from django.conf import settings
from cake.models import Post
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        """
        Инициализировать корзину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # сохранить текущий примененный купон
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """
        post_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        posts = Post.objects.filter(id__in=post_ids)
        cart = self.cart.copy()
        for post in posts:
            cart[str(post.id)]['post'] = post
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, post, quantity=1, override_quantity=False):
        """
        Добавить товар в корзину либо обновить его количество.
        """
        post_id = str(post.id)
        if post_id not in self.cart:
            self.cart[post_id] = {'quantity': 0, 'price': str(post.price)}
        if override_quantity:
            self.cart[post_id]['quantity'] = quantity
        else:
            self.cart[post_id]['quantity'] += quantity
        self.save()

    def save(self):
        # пометить сеанс как "измененный",
        # чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, post):
        """
        Удалить товар из корзины.
        """
        post_id = str(post.id)
        if post_id in self.cart:
            del self.cart[post_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        # удалить корзину из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
                * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def get_totalitem(self):
        totalitem = 0
        for p in self.cart:
            totalitem += 1
        return totalitem
