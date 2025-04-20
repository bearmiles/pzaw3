from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick = models.CharField(max_length=100, default='Unknown')
    id_user = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id_user:
            self.id_user = self.user.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.nick})" if self.nick else self.user.username
    
class Case(models.Model):
    name = models.CharField(max_length=100)

class Skin(models.Model):
    skin_name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=50)
    case = models.ForeignKey(Case , on_delete=models.CASCADE)
    skin_src = models.CharField(max_length=255, default="none")

class UserInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    obtained_at = models.DateTimeField(auto_now_add=True)