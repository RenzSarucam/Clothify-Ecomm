# Generated by Django 4.2.7 on 2023-11-21 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_payment_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='payment',
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='payment_method',
            field=models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Pick Up', 'Pick up'), ('Pending', 'Pending')], default='Pending', max_length=50),
        ),
    ]