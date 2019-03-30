from django.db import models
from django.urls import reverse
from django.utils import timezone
from  django.contrib.auth.models import User


class Category(models.Model):
    CatName = models.CharField(max_length=100)
    def __str__(self):
        return self.CatName

class Posts(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, default="1", on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='blog_pics')
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Blog-details", kwargs={"pk": self.id})
    
 