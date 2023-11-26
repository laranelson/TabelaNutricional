from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_desativacao = models.DateField()

    def desativar_usuario_se_necessario(self):
        data_atual = timezone.now().date()
        if data_atual >= self.data_desativacao:
            self.user.is_active = False
            self.user.save()
