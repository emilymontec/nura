# Corrige una fuga de datos entre usuarios: session_id era unique=True a
# nivel global, y el frontend usa 'default' como id inicial para todo el
# mundo, así que todos los usuarios terminaban compartiendo la misma fila
# de ChatSession. Ahora la unicidad es por (user, session_id).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_dataset_archived_dataset_archived_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatsession',
            name='session_id',
            field=models.CharField(max_length=120),
        ),
        migrations.AddConstraint(
            model_name='chatsession',
            constraint=models.UniqueConstraint(
                fields=('user', 'session_id'),
                name='unique_session_id_per_user',
            ),
        ),
    ]
