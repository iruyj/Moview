# Generated by Django 4.0.3 on 2022-03-14 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moview', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moviews',
            old_name='diary',
            new_name='story',
        ),
    ]