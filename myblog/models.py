from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField('is_admin', default=False, blank=True)
    profile_picture = models.ImageField(default="images/default_user_icon.jpg", null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    role = models.CharField(max_length=20, default='user', choices=[('author','author'), ('user','user')], blank=True)
    job = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=100,unique=True)

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('view_profile', kwargs={'pk': self.pk})
    
    def create_slug(self,*args, **kwargs):
        if not self.slug:
            self.slug= slugify(f'{self.username}-{self.email}')

            while User.objects.filter(slug=self.slug).exists():
                self.slug = slugify(f'{self.username}-{self.email}-{timezone.now().timestamp()}')

    def save(self, *args, **kwargs):
        self.create_slug()
        super().save(*args, **kwargs)
        
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    show_email = models.BooleanField(default=False)
    allow_view = models.BooleanField(default=False)
    email_notification = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s settings"

class Category(models.Model):
    name= models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_posts', args=[self.slug])

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='author_posts', on_delete=models.CASCADE)
    dop = models.DateField(auto_now_add=True)
    excerpt = models.CharField(max_length=300)
    article = models.TextField(null =True, blank=True)
    featured_image = models.ImageField(upload_to='images/', null=True, blank=True)
    featured_video = models.FileField(upload_to='videos/', null= True, blank=True)
    likes= models.ManyToManyField(User, related_name='posts', blank=True)
    category = models.ForeignKey(Category, related_name="posts", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, default='draft' , choices=[
        ('published','Published'),
        ('draft','Draft')
     ])
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a slug from the title
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Ensure uniqueness by adding a counter if needed
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)
        
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_body = models.TextField(null=True)
    date = models.DateField(default=timezone.now)
    is_verified = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"commented by {self.user} on {self.post}"

class Notification(models.Model):
    NOTIFY_TYPE =[
        ('new_post', 'New_Post'),
        ('like', 'Like'),
        ('comment','Comment'),
    ]

    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFY_TYPE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"