from django.contrib import admin
from .models import User, Post, Tag, Category,Comment, UserSettings, Notification

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserSettings)
admin.site.register(Notification)

