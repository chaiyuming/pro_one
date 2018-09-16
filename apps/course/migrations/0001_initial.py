# Generated by Django 2.0.6 on 2018-08-03 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CorseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('status', models.SmallIntegerField()),
                ('isstyle', models.SmallIntegerField(default=0)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('jobtitle', models.CharField(max_length=100)),
                ('profile', models.TextField()),
                ('avatar', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='PubCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video_url', models.URLField(default='')),
                ('cover_url', models.URLField()),
                ('price', models.FloatField()),
                ('durarion', models.IntegerField()),
                ('profile', models.TextField()),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.CorseCategory')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.CourseTeacher')),
            ],
        ),
        migrations.CreateModel(
            name='teacherCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='courseteacher',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.teacherCategory'),
        ),
        migrations.AddField(
            model_name='courseorder',
            name='order_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.PubCourse'),
        ),
    ]
