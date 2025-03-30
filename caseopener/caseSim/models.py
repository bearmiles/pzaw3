from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id_user:
            self.id_user = self.user.id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username