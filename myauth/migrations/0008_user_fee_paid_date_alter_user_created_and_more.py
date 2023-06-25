# Generated by Django 4.2.1 on 2023-06-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0007_alter_user_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fee_paid_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
