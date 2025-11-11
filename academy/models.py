from django.db import models
from django.contrib.auth.models import User

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.date}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=50)  # e.g., 'signals', 'classes'
    tier = models.CharField(max_length=100)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item_type} - {self.tier}"

class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
