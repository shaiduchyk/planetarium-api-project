import planetarium_service.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planetarium_service", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="astronomyshow",
            options={"ordering": ["-title"]},
        ),
        migrations.AlterModelOptions(
            name="reservation",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["row", "seat"]},
        ),
        migrations.AddField(
            model_name="planetariumdome",
            name="image",
            field=models.ImageField(
                null=True, upload_to=planetarium_service.models.movie_image_path
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("show_session", "row", "seat")},
        ),
    ]
