from django.db import models

# Create your models here.

"""
class Post:
    id int
    title star(50)
    content text
    created datetime
"""

class Post(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    created=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
