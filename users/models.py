from django.contrib.auth.models import User
from django.db import models

""" Perfil de usuario """
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    following = models.ManyToManyField(
        User, related_name='following', blank=True)
    friends = models.ManyToManyField(
        User, related_name='my_friends', blank=True)
    bio = models.CharField(default="", blank=True, null=True, max_length=350)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=6, blank=True, choices=(
        ('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Otro', 'Otro'),))
    orientation = models.CharField(max_length=12, blank=True, choices=(('Heterosexual', 'Heterosexual'), (
        'Homosexual', 'Homosexual'), ('Bisexual', 'Bisexual'), ('Pansexual', 'Pansexual'), ('Asexual', 'Asexual'), ('Otro', 'Otro'),))
    interests = models.ManyToManyField('Interest', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        default='default.jpg', upload_to='fotos_perfil_folder', blank=True, null=True)

    def profile_posts(self):
        return self.user.post_set.all()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return f'Perfil de {self.user.username}'


""" Intereses """
class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

""" Relación usuarios """
class Relationship(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='friend_sender')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='friend_receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
