from django.db import models
from datetime import timedelta

# Create your models here.
class Sapiens(models.Model):
    serial_id = models.CharField(max_length=10, unique=True)
    insti_id = models.CharField(max_length=50)
    name = models.CharField(max_length=300)
    allowed = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    total_count = models.IntegerField()
    issued_count = models.IntegerField()

    def __str__(self):
        return self.category_name
    
class Item(models.Model):
    serial_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class IssueRecord(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(Sapiens, on_delete=models.CASCADE)
    issue_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    expected_return = models.DateTimeField(auto_now=False, auto_now_add=False)
    return_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"IssueRecord - Item: {self.item}, User: {self.user}, Issue Time: {self.issue_time}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created for the first time
            self.expected_return = self.issue_time + timedelta(days=7)
        super(IssueRecord, self).save(*args, **kwargs)

