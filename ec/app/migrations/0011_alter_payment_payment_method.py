# Generated by Django 4.2.7 on 2023-11-22 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_payment_status_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Pick Up', 'Pick up')], default='Pending', max_length=50),
        ),
    ]
