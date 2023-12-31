# Generated by Django 5.0 on 2023-12-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeDTR', '0004_alter_employee_employee_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_type',
            field=models.CharField(choices=[('Party-Time', 'Part-Time'), ('Full-Time', 'Full-Time'), ('Flex-Time', 'Flex-Time'), ('Project-Based', 'Project-Based')], default='P', max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')]),
        ),
    ]
