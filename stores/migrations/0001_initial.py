# Generated by Django 3.1.7 on 2021-03-11 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('logo', models.ImageField(upload_to='stores')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('logo', models.ImageField(upload_to='stores')),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('profit_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.ingredient')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='store',
            name='ingredients',
            field=models.ManyToManyField(related_name='stores', through='stores.StoreIngredients', to='stores.Ingredient'),
        ),
        migrations.AddField(
            model_name='store',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
