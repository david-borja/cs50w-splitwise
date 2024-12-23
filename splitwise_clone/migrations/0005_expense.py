# Generated by Django 4.2 on 2024-12-01 17:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('splitwise_clone', '0004_alter_usergroup_description_alter_usergroup_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('amount', models.FloatField()),
                ('currency', models.CharField(choices=[('EUR', 'Euro'), ('USD', 'Us Dollar')], max_length=3)),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acquisitions', to='splitwise_clone.useralias')),
                ('splitters', models.ManyToManyField(related_name='shared_expenses', to='splitwise_clone.useralias')),
            ],
        ),
    ]
