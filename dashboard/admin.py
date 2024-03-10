from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(IssueRecord)
# Register your models here.
