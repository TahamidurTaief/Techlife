from django.core.management.base import BaseCommand
from blog_post.models import BlogPost
from PIL import Image
import io
import os
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = "Convert all existing uploaded images to WebP format"

    def handle(self, *args, **kwargs):
        posts = BlogPost.objects.exclude(featured_image="").exclude(featured_image=None)
        converted = 0
        for post in posts:
            try:
                if not post.featured_image.name.endswith(".webp"):
                    img = Image.open(post.featured_image.path)
                    output = io.BytesIO()
                    img.convert("RGB").save(output, "WEBP", quality=82)
                    output.seek(0)
                    new_name = os.path.splitext(post.featured_image.name)[0] + ".webp"
                    post.featured_image.save(
                        os.path.basename(new_name),
                        ContentFile(output.read()),
                        save=True,
                    )
                    converted += 1
                    self.stdout.write(f"Converted: {post.title}")
            except Exception as e:
                self.stdout.write(f"Failed: {post.title} - {e}")
        self.stdout.write(f"Done. Converted {converted} images.")
