# Generated by Django 4.2 on 2024-01-23 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeDTR', '0014_delete_payroll'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='system_id',
            field=models.IntegerField(null=True),
        ),
    ]
