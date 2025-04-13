from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post, Category, Tag, Gallery
from django.db.models import F
from django.core.mail import send_mail
from .forms import ContactForm, CommentForm
from cart.forms import CartAddProductForm, CartAddDesertForm
from .recommender import Recommender


class Home(ListView):
    model = Post
    template_name = 'cake/index.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Торты на заказ'
        return context


class PostsByCategory(ListView):
    template_name = 'cake/catalog.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False  # при запросе путстой категории выдает ошибку 404

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Post.objects.all().filter(category__slug=self.category.slug)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'cake/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False  # при запросе путстой категории выдает ошибку 404

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'cake/single.html'
    context_object_name = 'product_detail'

    def get_context_data(self, *, object_list=None, **kwargs):  # чтобы увеличить количество просмотров
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()  # берем данные views из бд т.к. в переменной выражение
        return context


class Search(ListView):
    template_name = 'cake/search.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):  # чтобы увеличить количество просмотров
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"  # передаем еще одну переменную для пагинации
        return context


class AboutDostavka(TemplateView):
    template_name = 'cake/dostavka.html'

    # context_object_name = 'dostavka'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка'
        return context


class AboutPolitics(TemplateView):
    template_name = 'cake/politics.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Политика конфиденциальности'
        return context


class AboutConditions(TemplateView):
    template_name = 'cake/conditions.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Условия оформления заказа'
        return context


def ContactForms(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'vanil-lnka@yandex.ru',
                             ['mihavxd@yandex.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('/contactforms/')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'cake/contact.html/', {"form": form})


def ProductDetail(request, id, slug):
    post = get_object_or_404(Post,
                             id=id,
                             slug=slug,
                             available=True)

    cart_product_form = CartAddProductForm()
    cart_desert_form = CartAddDesertForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([post], 4)

    comments = post.comments.filter(active=True)
    paginator = Paginator(comments, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    new_comment = None  # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            if new_comment:
                messages.success(request, 'Ваш комментарий ожидает модерации')
                send_mail(subject='Отзыв Ванилинка дебаг',
                          message='Оставлен новый отзыв на сайте Ванилинка',
                          from_email='vanil-lnka@yandex.ru',
                          recipient_list=['mihavxd@yandex.ru'],
                          fail_silently=True)
                return redirect(request.path)
            else:
                messages.error(request, 'Ошибка отправки комментария')
        else:
            messages.error(request, 'Заполните все поля')
    else:
        comment_form = CommentForm()
    return render(request,
                  'cake/single.html',
                  {'post': post,
                   'page_obj': page_obj,

                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'cart_product_form': cart_product_form,
                   'cart_desert_form': cart_desert_form,
                   'recommended_products': recommended_products})