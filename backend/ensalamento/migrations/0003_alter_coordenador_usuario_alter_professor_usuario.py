
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            'ensalamento',
            '0002_remove_coordenador_email_remove_coordenador_senha_and_more',
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Torna obrigatório o usuário do coordenador.
        migrations.AlterField(
            model_name='coordenador',
            name='usuario',
            field=models.OneToOneField(
                limit_choices_to={'tipo': 'COORDENADOR'},
                on_delete=django.db.models.deletion.CASCADE,
                related_name='coordenador',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Torna obrigatório o usuário do professor.
        migrations.AlterField(
            model_name='professor',
            name='usuario',
            field=models.OneToOneField(
                limit_choices_to={'tipo': 'PROFESSOR'},
                on_delete=django.db.models.deletion.CASCADE,
                related_name='professor',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Torna obrigatório o semestre da turma.
        migrations.AlterField(
            model_name='turma',
            name='semestre',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='turmas',
                to='ensalamento.semestre',
            ),
        ),
    ]
