# Generated by Django 3.2.9 on 2022-01-04 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_restaurnt_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressuser',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.address'),
        ),
    ]