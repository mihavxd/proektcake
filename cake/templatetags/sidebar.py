from django import template
from cake.models import Post, Tag

register = template.Library()

@register.inclusion_tag('cake/popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt] #сортируем по просмотру и срезаем последние три и так формируем наиболее популярный
    return {"posts": posts}

@register.inclusion_tag('cake/tags_tpl.html')
# def get_tags(cnt=10):
#     tags = Tag.objects.order_by('-posts')[:cnt] #сортируем по просмотру и срезаем последние три и так формируем наиболее популярный
def get_tags():
    tags = Tag.objects.all()
    return {"tags": tags}
