# Generated by Django 4.1.7 on 2023-04-09 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tuition_app', '0017_study_material_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='mark_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_date', models.DateField()),
                ('exam_title', models.TextField(max_length=150)),
                ('mark', models.CharField(max_length=50)),
                ('total', models.CharField(max_length=100)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.batch_table')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.course_table')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.student_table')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.teacher_table1')),
            ],
        ),
    ]
