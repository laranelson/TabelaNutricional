# management/commands/desativar_usuarios.py

from django.core.management.base import BaseCommand
from core.models import UserProfile  # Substitua 'your_app' pelo nome de sua aplicação
from django.utils import timezone


class Command(BaseCommand):
    help = 'Desativa os usuários com base na data de desativação definida no perfil'

    def handle(self, *args, **options):
        usuarios_para_desativar = UserProfile.objects.filter(data_desativacao__lte=timezone.now().date())

        for perfil in usuarios_para_desativar:
            perfil.desativar_usuario_se_necessario()
            self.stdout.write(self.style.SUCCESS(f'O usuário {perfil.user.username} foi desativado.'))

        self.stdout.write(self.style.SUCCESS('Usuários desativados com sucesso.'))
