# Generated by Django 5.1.5 on 2025-01-23 01:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy_management_app', '0004_suppliers_purchase_created_at_purchase_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='pharmacy_management_app.suppliers'),
            preserve_default=False,
        ),
    ]
