# Generated by Django 4.2.1 on 2023-05-13 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "name",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("description", models.CharField(max_length=100)),
                ("url", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("business", "business"),
                            ("entertainment", "entertainment"),
                            ("general", "general"),
                            ("health", "health"),
                            ("science", "science"),
                            ("sports", "sports"),
                            ("technology", "technology"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("ar", "ar"),
                            ("de", "de"),
                            ("en", "en"),
                            ("es", "es"),
                            ("fr", "fr"),
                            ("he", "he"),
                            ("it", "it"),
                            ("nl", "nl"),
                            ("no", "no"),
                            ("pt", "pt"),
                            ("ru", "ru"),
                            ("sv", "sv"),
                            ("ud", "ud"),
                            ("zh", "zh"),
                        ],
                        max_length=5,
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        choices=[
                            ("ae", "ae"),
                            ("ar", "ar"),
                            ("at", "at"),
                            ("au", "au"),
                            ("be", "be"),
                            ("bg", "bg"),
                            ("br", "br"),
                            ("ca", "ca"),
                            ("ch", "ch"),
                            ("cn", "cn"),
                            ("co", "co"),
                            ("cu", "cu"),
                            ("cz", "cz"),
                            ("de", "de"),
                            ("eg", "eg"),
                            ("fr", "fr"),
                            ("gb", "gb"),
                            ("gr", "gr"),
                            ("hk", "hk"),
                            ("hu", "hu"),
                            ("id", "id"),
                            ("ie", "ie"),
                            ("il", "il"),
                            ("in", "in"),
                            ("it", "it"),
                            ("jp", "jp"),
                            ("kr", "kr"),
                            ("lt", "lt"),
                            ("lv", "lv"),
                            ("ma", "ma"),
                            ("mx", "mx"),
                            ("my", "my"),
                            ("ng", "ng"),
                            ("nl", "nl"),
                            ("no", "no"),
                            ("nz", "nz"),
                            ("ph", "ph"),
                            ("pl", "pl"),
                            ("pt", "pt"),
                            ("ro", "ro"),
                            ("rs", "rs"),
                            ("ru", "ru"),
                            ("sa", "sa"),
                            ("se", "se"),
                            ("sg", "sg"),
                            ("si", "si"),
                            ("sk", "sk"),
                            ("th", "th"),
                            ("tr", "tr"),
                            ("tw", "tw"),
                            ("ua", "ua"),
                            ("us", "us"),
                            ("ve", "ve"),
                            ("za", "za"),
                        ],
                        max_length=5,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("author", models.CharField(max_length=100, null=True)),
                (
                    "title",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("description", models.CharField(max_length=100, null=True)),
                ("url", models.CharField(max_length=100, null=True)),
                ("published_at", models.DateField()),
                ("content", models.CharField(max_length=1000)),
                ("top_headline", models.BooleanField(default=False)),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articles",
                        to="news.source",
                    ),
                ),
            ],
        ),
    ]
