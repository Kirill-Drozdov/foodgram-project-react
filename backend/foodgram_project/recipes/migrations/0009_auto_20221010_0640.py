# Generated by Django 2.2.16 on 2022-10-10 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20221010_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Название ингредиента'),
        ),
    ]