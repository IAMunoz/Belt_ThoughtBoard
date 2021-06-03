from django.db import models
from apps.login.models import User




class Thought(models.Model):
    title = models.TextField(max_length=1000, blank=False, null=False)
    poster = models.ForeignKey(User, related_name='thoughts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'{self.owner.name}\'s thougth: {self.title}'

class Like(models.Model):
    owner = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    thought = models.ForeignKey(Thought, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
