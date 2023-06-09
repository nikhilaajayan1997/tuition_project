# Generated by Django 4.1.7 on 2023-04-17 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tuition_app', '0027_task_submitted_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.TextField(max_length=50)),
                ('subject', models.TextField(max_length=50)),
                ('feedback', models.TextField(max_length=500)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.student_table')),
            ],
        ),
    ]
