# Generated by Django 5.2 on 2025-05-18 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0006_remove_grade_probability"),
    ]

    operations = [
        migrations.RenameField(
            model_name="trade",
            old_name="traded_at",
            new_name="created_at",
        ),
        migrations.RemoveField(
            model_name="trade",
            name="buyer",
        ),
        migrations.AddField(
            model_name="trade",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name="TradeRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_approved", models.BooleanField(null=True)),
                ("requested_at", models.DateTimeField(auto_now_add=True)),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buy_requests",
                        to="cards.user",
                    ),
                ),
                (
                    "trade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cards.trade"
                    ),
                ),
            ],
        ),
    ]
