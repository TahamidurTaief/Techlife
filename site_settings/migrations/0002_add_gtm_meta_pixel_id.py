from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("site_settings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="gtm_id",
            field=models.CharField(blank=True, help_text="Google Tag Manager ID (e.g., GTM-XXXXXXX)", max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="meta_pixel_id",
            field=models.CharField(blank=True, help_text="Meta Pixel ID (e.g., 1234567890)", max_length=50, null=True),
        ),
    ]
