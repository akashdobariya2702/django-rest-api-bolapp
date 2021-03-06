# Generated by Django 2.0 on 2020-04-23 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('client_id', models.CharField(max_length=250)),
                ('client_secret', models.TextField()),
            ],
            options={
                'verbose_name': 'Shop Detail',
                'verbose_name_plural': 'Shop Details',
            },
        ),
    ]
