# Generated by Django 3.2.12 on 2024-02-13 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_blog_alter_project_link_blog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='link_blog',
        ),
    ]