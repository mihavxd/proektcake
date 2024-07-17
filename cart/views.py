from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from cake.models import Post
from .cart import Cart
from .forms import CartAddProductForm
from cake.recommender import Recommender
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, post_id):
    cart = Cart(request)
    post = get_object_or_404(Post, id=post_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(post=post,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, post_id):
    cart = Cart(request)
    post = get_object_or_404(Post, id=post_id)
    cart.remove(post)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['post'] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'coupon_apply_form': coupon_apply_form,
                                                'recommended_products': recommended_products})
