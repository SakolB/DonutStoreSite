# Generated by Django 4.2.2 on 2023-08-07 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_order_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='orders',
        ),
        migrations.AddField(
            model_name='order',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.profile'),
        ),
    ]
