from django.db import models
from django.contrib.auth.models import User
import uuid

def user_pdf_upload_path(instance, filename):
    return f'user_{instance.owner.id}/pdfs/{filename}'

class PDFFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdf_files')
    file = models.FileField(upload_to=user_pdf_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ShareLink(models.Model):
    pdf = models.ForeignKey(PDFFile, on_delete=models.CASCADE, related_name='share_links')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ShareLink for {self.pdf.name}"

class Comment(models.Model):
    pdf = models.ForeignKey(PDFFile, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    invited_user_name = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user or self.invited_user_name} on {self.pdf.name}'
from django.db import models

# Create your models here.
