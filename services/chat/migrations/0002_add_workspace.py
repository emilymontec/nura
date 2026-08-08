# CORRECCIÓN (Módulo 1): esta migración originalmente volvía a crear el
# modelo Workspace y el campo ChatSession.workspace, pero 0001_initial ya
# los creaba. Eso hacía que `python manage.py migrate` fallara con
# "table chat_workspace already exists" en cualquier base de datos nueva,
# es decir, el proyecto no podía instalarse desde cero.
#
# Se deja como no-op (sin operaciones) para no romper la cadena de
# dependencias de las migraciones 0003/0004/0005 que ya dependen de esta.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = []
