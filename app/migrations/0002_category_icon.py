# Generated by Django 4.1.5 on 2023-05-31 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
