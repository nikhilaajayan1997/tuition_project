# Generated by Django 4.1.7 on 2023-04-08 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tuition_app', '0015_attendence'),
    ]

    operations = [
        migrations.CreateModel(
            name='syllabus_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.CharField(max_length=50)),
                ('topic', models.TextField(max_length=500)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.batch_table')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.course_table')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.teacher_table1')),
            ],
        ),
    ]
