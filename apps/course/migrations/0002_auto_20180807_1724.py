# Generated by Django 2.0.6 on 2018-08-07 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseteacher',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='teacher', to='course.teacherCategory'),
        ),
        migrations.AlterField(
            model_name='pubcourse',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='course', to='course.CorseCategory'),
        ),
    ]
