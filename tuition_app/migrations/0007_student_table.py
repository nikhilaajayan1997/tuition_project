# Generated by Django 4.1.7 on 2023-04-06 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tuition_app', '0006_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='student_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(max_length=250)),
                ('phone', models.CharField(max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/')),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.batch_table')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
