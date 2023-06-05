from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

""" Post """
class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Título')
    content = RichTextField(blank=True, null=True, verbose_name='Cuerpo')
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="blogpost", blank=True)
    saves = models.ManyToManyField(User, related_name="blogsave", blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_saves(self):
        return self.saves.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})


""" Comentario """
class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name="blogcomment", blank=True)
    reply = models.ForeignKey(
        'self', null=True, related_name="replies", on_delete=models.CASCADE)

    def total_clikes(self):
        return self.likes.count()

    def __str__(self):
        return '%s - %s - %s' % (self.post.title, self.name, self.id)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})
