# Generated by Django 3.2.9 on 2022-01-06 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_email'),
        ('restaurant', '0005_alter_orderstatus_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressuser',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
        ),
    ]