# Generated by Django 3.1.1 on 2020-09-14 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ownerblog',
            options={'ordering': ['-date_added']},
        ),
    ]
