from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, default=None)
    email = models.EmailField(max_length=255,blank=False)
    password = models.CharField(blank=False,max_length=10)
    name = models.CharField(max_length=20 , blank=False)
    age = models.SmallIntegerField()
    phoneNo = models.CharField(max_length=11, blank=False)
   


class Blog(models.Model):
    title = models.CharField(max_length=60, blank=False)
    img = models.ImageField(upload_to='Images/')
    content = models.TextField()
    creationDate = models.DateTimeField( blank=False)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="The author who created the blog")


    class Meta:
        ordering = ['creationDate']
   

    

# Create your models here.
