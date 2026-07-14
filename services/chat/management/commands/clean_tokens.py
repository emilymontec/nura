from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Limpia tokens de autenticación viejos de la base de datos"

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Eliminar tokens más viejos que N días (predeterminado: 7)',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)

        # Limpiar tokens de rest_framework_simplejwt (BlacklistedToken y OutstandingToken)
        try:
            from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
            
            # Eliminar tokens vencidos
            outstanding_expired = OutstandingToken.objects.filter(expires_at__lt=timezone.now())
            count_outstanding = outstanding_expired.count()
            outstanding_expired.delete()
            
            # Eliminar tokens blacklisted viejos
            blacklisted_old = BlacklistedToken.objects.filter(blacklisted_at__lt=cutoff_date)
            count_blacklisted = blacklisted_old.count()
            blacklisted_old.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Limpiados {count_outstanding} tokens vencidos y {count_blacklisted} tokens en lista negra.'
                )
            )
        except ImportError:
            self.stdout.write(
                self.style.WARNING('rest_framework_simplejwt no está instalado o no está configurado.')
            )

        # Limpiar sesiones de Django
        try:
            from django.contrib.sessions.models import Session
            expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
            count_sessions = expired_sessions.count()
            expired_sessions.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Limpiadas {count_sessions} sesiones expiradas.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'No se pudieron limpiar sesiones: {e}')
            )

        self.stdout.write(self.style.SUCCESS('Limpieza de tokens completada!'))
