# Generated by Django 4.2.3 on 2023-08-20 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_remove_listing_buyer"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="subtitle",
            field=models.CharField(max_length=64, null=True),
        ),
    ]