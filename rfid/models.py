from django.db import models

class AccessToken(models.Model):
    access_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    scanner_name = models.CharField(max_length=100)
    scanner_uid = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"Scan {self.id}: {self.scanner_name}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is being created
            # Set scanner_name based on object count
            scanner_count = AccessToken.objects.count() + 1
            self.scanner_name = f"Scanner {scanner_count}"
        super().save(*args, **kwargs)
