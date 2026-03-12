from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUserModel
import hashlib
from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUserModel
from tags.models import Tag
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    font_awesome_icon = models.CharField(default="fa-solid fa-layer-group", max_length=100, null=True, blank=True, verbose_name="Fontawesome icon", help_text="e.g: fa-solid fa-layer-group", error_messages="Enter valid class of fontawesome icon")
    # description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure the slug is unique
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # While the generated slug exists in the database, keep adding a counter
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Parent Category"
    )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = 'SubCategories'
        ordering = ['category__name', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while SubCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
import re
import hashlib
import logging
from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

logger = logging.getLogger(__name__)


def _strip_html(text: str) -> str:
    clean = re.sub(r'<[^>]+>', '', str(text))
    return ' '.join(clean.split()).strip()


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending Approval"),
        ("published", "Published"),
        ("rejected", "Rejected"),
    )

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = RichTextUploadingField()
    featured_image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    featured_image_thumbnail = ImageSpecField(
        source='featured_image',
        processors=[ResizeToFill(550, 380), Adjust(sharpness=1)],
        format='WEBP',
        options={'quality': 90}
    )
    featured_image_url = models.URLField(max_length=500, null=True, blank=True)

    content_hash = models.CharField(
        max_length=64, editable=False, db_index=True, null=True, blank=True
    )
    image_hash = models.CharField(
        max_length=64, editable=False, db_index=True, null=True, blank=True
    )
    description_hash = models.CharField(          # ← নতুন field
        max_length=64, editable=False, db_index=True, null=True, blank=True
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name="Sub Category"
    )
    author = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name='authored_posts'
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    views = models.PositiveIntegerField(default=0)
    content_quality = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name="blog_posts")

    def save(self, *args, **kwargs):
        kwargs.pop('skip_auto_status', False)

        # ── Slug generation ───────────────────────────────────────────────
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # ── Description hash (HTML stripped) ─────────────────────────────
        clean_desc = _strip_html(self.description)
        self.description_hash = hashlib.md5(clean_desc.encode("utf-8")).hexdigest()

        # ── Content hash (title + clean description) ──────────────────────
        self.content_hash = hashlib.md5(
            (self.title + clean_desc).encode("utf-8")
        ).hexdigest()

        # ── Image hash ────────────────────────────────────────────────────
        if self.featured_image:
            try:
                self.featured_image.file.seek(0)
                img_bytes = self.featured_image.file.read()
                self.image_hash = hashlib.md5(img_bytes).hexdigest()
                self.featured_image.file.seek(0)
            except Exception as e:
                logger.error(f"Image hash generation error: {e}")

        super().save(*args, **kwargs)

    @property
    def total_reactions(self):
        return self.reactions.count()

    def reaction_breakdown(self):
        return self.reactions.values("reaction_type").annotate(
            total=models.Count("reaction_type")
        )

    def __str__(self):
        return f"{self.title} created by {self.author}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'



class Like(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "post",
            "user",
        )  # akta user double like dite parbena 1 ta post er jonno
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.first_name} liked {self.post.title}"


class BlogAdditionalImage(models.Model):
    blog = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="additional_images"
    )
    additional_image = models.ImageField(
        upload_to="blog_images/additional/", null=True, blank=True
    )
    additional_image_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Image for {self.blog.title}"


class Review(models.Model):
    RATING_CHOICES = (
        (1, " 1 - Very Bad"),
        (2, " 2 - Bad"),
        (3, " 3 - Average"),
        (4, " 4 - Good"),
        (5, " 5 - Excellent"),
    )

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "post",
            "user",
        )  # akta user double review dite parbena 1 ta post er jonno
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.first_name} rated {self.rating}⭐ on {self.post.title}"

# view count system (Ip tracking)
class Post_view_ip(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="view_track"
    )
    user = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, null=True, blank=True
    )
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    viewed_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "ip_address")

    def __str__(self):
        return f"{self.post.title} viewed by {self.user or self.ip_address}"


class compnay_logo(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    company_image = models.ImageField(
        upload_to="company/image", null=True, blank=True
    )
    company_image_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
    




