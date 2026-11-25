
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensalamento', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Remove os campos antigos de autenticação.
        migrations.RemoveField(
            model_name='coordenador',
            name='email',
        ),
        migrations.RemoveField(
            model_name='coordenador',
            name='senha',
        ),
        migrations.RemoveField(
            model_name='professor',
            name='email',
        ),
        migrations.RemoveField(
            model_name='professor',
            name='senha',
        ),

        # Remove ano e período diretamente da turma.
        migrations.RemoveField(
            model_name='turma',
            name='ano',
        ),
        migrations.RemoveField(
            model_name='turma',
            name='periodo',
        ),

        # Cria os relacionamentos temporariamente opcionais.
        migrations.AddField(
            model_name='coordenador',
            name='usuario',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='coordenador',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='professor',
            name='usuario',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='professor',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Cria a entidade Semestre.
        migrations.CreateModel(
            name='Semestre',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('ano', models.PositiveIntegerField()),
                ('periodo', models.PositiveIntegerField()),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
            ],
            options={
                'db_table': 'semestre',
                'constraints': [
                    models.CheckConstraint(
                        condition=models.Q(
                            ('data_fim__gt', models.F('data_inicio'))
                        ),
                        name='ck_semestre_fim_apos_inicio',
                    ),
                    models.UniqueConstraint(
                        fields=('ano', 'periodo'),
                        name='uq_semestre_ano_periodo',
                    ),
                ],
            },
        ),

        # Cria o relacionamento temporariamente opcional.
        migrations.AddField(
            model_name='turma',
            name='semestre',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='turmas',
                to='ensalamento.semestre',
            ),
        ),

        # Cria a entidade Solicitação de Troca.
        migrations.CreateModel(
            name='SolicitacaoTroca',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('motivo', models.CharField(max_length=255)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('PENDENTE', 'Pendente'),
                            ('APROVADA', 'Aprovada'),
                            ('RECUSADA', 'Recusada'),
                        ],
                        default='PENDENTE',
                        max_length=20,
                    ),
                ),
                (
                    'tipo_troca',
                    models.CharField(
                        choices=[
                            ('SALA', 'Sala'),
                            ('HORARIO', 'Horário'),
                            ('AMBOS', 'Sala e Horário'),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    'alocacao_destino',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='solicitacoes_destino',
                        to='ensalamento.alocacao',
                    ),
                ),
                (
                    'alocacao_origem',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='solicitacoes_origem',
                        to='ensalamento.alocacao',
                    ),
                ),
                (
                    'professor_solicitante',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='solicitacoes_troca',
                        to='ensalamento.professor',
                    ),
                ),
            ],
            options={
                'db_table': 'solicitacao_troca',
            },
        ),

        # Relaciona o histórico às solicitações de troca.
        migrations.AddField(
            model_name='historico',
            name='solicitacao_troca',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='historicos',
                to='ensalamento.solicitacaotroca',
            ),
        ),
    ]
