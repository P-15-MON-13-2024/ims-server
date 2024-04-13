from django.db import models
from datetime import datetime, timedelta

class Sapien(models.Model):
    serial_id = models.CharField(max_length=10, unique=True)
    insti_id = models.CharField(max_length=50)
    name = models.CharField(max_length=300)
    allowed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Bucket(models.Model):
    bucket_name = models.CharField(max_length=100, unique=True)
    total_count = models.IntegerField(default=0)
    issued_count = models.IntegerField(default=0)

    def __str__(self):
        return self.bucket_name
    
class Item(models.Model):
    serial_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def get_latest_issue_record(self):
        latest_issue_record = self.issuerecord_set.filter(is_returned=False).order_by('-issue_time').first()
        return latest_issue_record

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.category.total_count += 1
            self.category.save()
        super(Item, self).save(*args, **kwargs)


class IssueRecord(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(Sapien, on_delete=models.CASCADE)
    issue_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    expected_return = models.DateTimeField(auto_now=False, auto_now_add=False)
    return_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Item: {self.item}, User: {self.user}, Issue Time: {self.issue_time}"

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.issue_time = datetime.now()
            self.expected_return = datetime.now() + timedelta(days=7)
        super(IssueRecord, self).save(*args, **kwargs)

