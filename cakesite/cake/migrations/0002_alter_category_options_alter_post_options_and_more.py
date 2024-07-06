# Generated by Django 4.1.2 on 2024-01-29 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'verbose_name': 'Категория (ю)', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['title'], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['title'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AddField(
            model_name='post',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['title'], name='cake_catego_title_f04e06_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['id', 'slug'], name='cake_post_id_84ba6a_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['title'], name='cake_post_title_04ed11_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-created_at'], name='cake_post_created_a1777d_idx'),
        ),
    ]
