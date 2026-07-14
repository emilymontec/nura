from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone


class Command(BaseCommand):
    help = "Realiza una consulta simple para mantener activa la conexión a la base de datos"

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Consulta muy simple para mantener la conexión activa
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Keep-alive ejecutado exitosamente a las {timezone.now().strftime("%Y-%m-%d %H:%M:%S")} UTC'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error en keep-alive: {str(e)}'
                )
            )
