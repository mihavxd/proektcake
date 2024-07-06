from django.urls import path
from .views import *
from .sitemap import StaticViewsSitemap, DynamicViewsSitemap
from django.contrib.sitemaps.views import sitemap
from .feeds import LatestCakeFeed





urlpatterns = [
    path('', Home.as_view(), name='home'),
    #path('', PostsByCategory.as_view(), name='product_list'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('<int:id>/<slug:slug>/', ProductDetail, name='product_detail'),
    #path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('dostavka/', AboutDostavka.as_view(), name='dostavka'),
    path('contactforms/', ContactForms, name='contactforms'),
    path('politics/', AboutPolitics.as_view(), name='politics'),
    path('conditions/', AboutConditions.as_view(), name='conditions'),
    path("feed/rss", LatestCakeFeed(), name="cake_feed"),
]