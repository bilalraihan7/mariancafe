# Generated by Django 4.2.7 on 2024-03-02 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0030_alter_checkout_checkout_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodmenu',
            name='removalStatus',
            field=models.BooleanField(default=False),
        ),
    ]