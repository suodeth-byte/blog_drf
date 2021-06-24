from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return """{}| (By {})::: {} """.format(self.title, self.author, self.content)

    # def get_absolute_url(self):
    #     return reverse('article-detail', args=(str(self.pk)))

###############################################################
## web part ##
