from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='archivo',
            field=models.FileField(default='documentos/placeholder.txt', upload_to='documentos/', verbose_name='Archivo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='documento',
            name='esta_firmado',
            field=models.BooleanField(default=False, verbose_name='¿Está firmado?'),
        ),
        migrations.AddField(
            model_name='documento',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True, verbose_name='Última actualización'),
        ),
        migrations.AddField(
            model_name='documento',
            name='fecha_carga',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de carga'),
        ),
        migrations.AddField(
            model_name='documento',
            name='hash_sha256',
            field=models.CharField(blank=True, max_length=64, verbose_name='Hash SHA-256'),
        ),
        migrations.AddField(
            model_name='documento',
            name='titulo',
            field=models.CharField(default='Documento sin título', max_length=200, verbose_name='Título'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documentos_files', to=settings.AUTH_USER_MODEL, verbose_name='Propietario'),
        ),
        migrations.AlterModelOptions(
            name='documento',
            options={'ordering': ['-fecha_carga'], 'verbose_name': 'Documento', 'verbose_name_plural': 'Documentos'},
        ),
    ]
