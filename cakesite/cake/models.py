from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория (ю)'
        verbose_name_plural = 'Категории'
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
        ]


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)
    content = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')  # связываем один ко многим
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')  # Многие ко многим

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    # return reverse('post', kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    class Meta:
        verbose_name = 'Торт'
        verbose_name_plural = 'Торты'
        ordering = ['title']  # сортировка по созданию - свежие были выши
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['title']),
            models.Index(fields=['-created_at']),
        ]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, verbose_name='Ваше имя')
    email = models.EmailField(verbose_name='Адрес электронной почты')
    body = models.TextField(max_length=500, verbose_name='Текст отзыва')
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
