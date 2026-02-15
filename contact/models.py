from django.db import models
from accounts.models import CustomUserModel
class contact_or_support(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="contact_user", null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    


class FooterSettings(models.Model):
    # Logo & About
    logo = models.ImageField(upload_to='footer/', help_text="Upload the Techlife-bd Logo")
    description = models.TextField(help_text="The short 'About Us' text in the footer")
    
    # Contact Info
    email = models.EmailField(default="contact@techlife.com")
    phone = models.CharField(max_length=20, default="+8801700895489")
    address = models.TextField(default="Green Road, Dhaka")

    # Social Media Links
    facebook_url = models.URLField(blank=True, null=True, help_text="Facebook profile link")
    twitter_url = models.URLField(blank=True, null=True, help_text="Twitter/X profile link")
    linkedin_url = models.URLField(blank=True, null=True, help_text="LinkedIn profile link")
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True, help_text="WhatsApp number with country code")

    # Developer Info
    developer_company_name = models.CharField(max_length=100, default="Intelligent Systems & Solution Limited")
    developer_company_url = models.URLField(default="#")


    class Meta:
        verbose_name = "Footer Setting"
        verbose_name_plural = "Footer Settings"

    def __str__(self):
        return "Global Footer Configuration"
