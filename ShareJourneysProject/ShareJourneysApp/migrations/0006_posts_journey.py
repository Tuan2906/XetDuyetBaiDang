# Generated by Django 5.0.3 on 2024-06-20 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShareJourneysApp', '0005_posts_user_nv_alter_posts_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='journey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ShareJourneysApp.journey'),
        ),
    ]
