# Generated by Django 4.1.7 on 2023-04-08 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tuition_app', '0014_tuition_table1_tuition_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_date', models.DateField()),
                ('status', models.CharField(max_length=20)),
                ('tuition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition_app.tuition_table1')),
            ],
        ),
    ]
