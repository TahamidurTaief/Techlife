from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog_post", "0003_alter_blogpost_featured_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="meta_title",
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="meta_description",
            field=models.CharField(blank=True, max_length=160),
        ),
    ]
