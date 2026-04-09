# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .manager import CustomUserManager
import random
from django.conf import settings
import io
import os
from django.core.files.base import ContentFile
from PIL import Image

class CustomUserModel(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    address_line_1 = models.CharField(null=True, blank=True, max_length=100)
    address_line_2 = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=20)
    postcode = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    mobile = models.CharField(null=True, blank=True, max_length=15)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="user_profile", default="user_profile/default_user_profile.png")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username = None

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.profile_picture and hasattr(self.profile_picture, "file"):
            try:
                img = Image.open(self.profile_picture)
                if img.format != "WEBP":
                    output = io.BytesIO()
                    img = img.convert("RGB")
                    img.save(output, format="WEBP", quality=82, method=6)
                    output.seek(0)
                    original_name = os.path.splitext(self.profile_picture.name)[0]
                    self.profile_picture = ContentFile(
                        output.read(),
                        name=f"{os.path.basename(original_name)}.webp",
                    )
            except Exception:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class EmailVerificationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    purpose = models.CharField(max_length=20, default="verify")  # verify/reset

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)
