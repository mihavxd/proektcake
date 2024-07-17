from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from cake.models import Post


class LatestCakeFeed(Feed):
    title = "Ванилинка Торты на заказ"
    link = ""
    description = "Торты на заказ по индивидуальным проектам."

    def items(self):
        return Post.objects.order_by("-created_at")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)
