import redis
from django.conf import settings
from .models import Post

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender:
    def get_product_key(self, id):
        return f'post:{id}:purchased_with'

    def products_bought(self, posts):
        post_ids = [p.id for p in posts]
        for post_id in post_ids:
            for with_id in post_ids:
                # получить другие товары, купленные
                # вместе с каждым товаром
                if post_id != with_id:
                    # увеличить балл товара,
                    # купленного вместе
                    r.zincrby(self.get_product_key(post_id), 1, with_id)

    def suggest_products_for(self, posts, max_results=6):
        post_ids = [p.id for p in posts]
        if len(posts) == 1:
            # только 1 товар
            suggestions = r.zrange(
                self.get_product_key(post_ids[0]),
                0, -1, desc=True)[:max_results]
        else:
            # сгенерировать временный ключ
            flat_ids = ''.join([str(id) for id in post_ids])
            tmp_key = f'tmp_{flat_ids}'
            # несколько товаров, объединить баллы всех товаров
            # сохранить полученное сортированное множество
            # во временном ключе
            keys = [self.get_product_key(id) for id in post_ids]
            r.zunionstore(tmp_key, keys)
            # удалить идентификаторы товаров,
            # для которых дается рекомендация
            r.zrem(tmp_key, *post_ids)
            # получить идентификаторы товаров по их количеству,
            # сортировка по убыванию
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            # удалить временный ключ
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # получить предлагаемые товары и
        # отсортировать их по порядку их появления
        suggested_products = list(Post.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Post.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
