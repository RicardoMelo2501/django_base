# Generated by Django 4.2.2 on 2023-07-14 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20230702_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='arquivo_pdf',
            field=models.FileField(default=None, max_length=250, null=True, upload_to='licitacoes/'),
        ),
    ]
