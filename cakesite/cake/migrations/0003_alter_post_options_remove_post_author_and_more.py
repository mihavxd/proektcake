# Generated by Django 4.1.2 on 2024-01-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake', '0002_alter_category_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['title'], 'verbose_name': 'Торт', 'verbose_name_plural': 'Торты'},
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.AlterField(
            model_name='post',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Наличие'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
    ]
