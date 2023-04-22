from django.db import models
from django.contrib.auth.models import User


class course_table(models.Model):
    course_name=models.CharField(max_length=200)
    course_fee=models.CharField(max_length=20)

class batch_table(models.Model):
    batch_name=models.CharField(max_length=120)

class teacher_table(models.Model):
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
    address=models.TextField(max_length=250)
    phone=models.CharField(max_length=15)
    image=models.ImageField(null=True,blank=True,upload_to='image/')

class teacher_table1(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
    address=models.TextField(max_length=250)
    phone=models.CharField(max_length=15)
    image=models.ImageField(null=True,blank=True,upload_to='image/')

class student_table(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    batch=models.ForeignKey(batch_table,on_delete=models.CASCADE,null=True)
    address=models.TextField(max_length=250)
    phone=models.CharField(max_length=15)
    image=models.ImageField(null=True,blank=True,upload_to='image/')

class tuition_table(models.Model):
    student=models.ForeignKey(student_table,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)

class tuition_table1(models.Model):
    student=models.ForeignKey(student_table,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
    batch=models.ForeignKey(batch_table,on_delete=models.CASCADE,null=True)



class timetable_table(models.Model):
    teacher=models.ForeignKey(teacher_table1,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
    batch=models.ForeignKey(batch_table,on_delete=models.CASCADE,null=True)
    day=models.CharField(max_length=50)
    time_from=models.CharField(max_length=50)
    time_to=models.CharField(max_length=50)

class stud_leave_table(models.Model):
    student=models.ForeignKey(student_table,on_delete=models.CASCADE,null=True)
    subject=models.CharField(max_length=120)
    message=models.TextField(max_length=500)
    date=models.DateField(auto_now_add=True)
    leave_date=models.DateField()
    status=models.CharField(max_length=25,null=True)

class teacher_leave_table(models.Model):
    teacher=models.ForeignKey(teacher_table1,on_delete=models.CASCADE,null=True)
    subject=models.CharField(max_length=120)
    message=models.TextField(max_length=500)
    date=models.DateField(auto_now_add=True)
    leave_date=models.DateField()
    status=models.CharField(max_length=25,null=True)

class attendence(models.Model):
    tuition=models.ForeignKey(tuition_table1,on_delete=models.CASCADE,null=True)
    class_date=models.DateField()
    status=models.CharField(max_length=20)

class syllabus_table(models.Model):
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
    batch=models.ForeignKey(batch_table,on_delete=models.CASCADE,null=True)
    teacher=models.ForeignKey(teacher_table1,on_delete=models.CASCADE,null=True)
    chapter=models.CharField(max_length=50)
    topic=models.TextField(max_length=500)

class study_material_table(models.Model):
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
    batch=models.ForeignKey(batch_table,on_delete=models.CASCADE,null=True)
    teacher=models.ForeignKey(teacher_table1,on_delete=models.CASCADE,null=True)
    topic=models.TextField(max_length=500)
    document=models.FileField(upload_to='doc/')

class mark_table(models.Model):
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
    batch=models.ForeignKey(batch_table,on_delete=models.CASCADE,null=True)
    teacher=models.ForeignKey(teacher_table1,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(student_table,on_delete=models.CASCADE,null=True)
    exam_date=models.DateField()
    exam_title=models.TextField(max_length=150)
    mark=models.CharField(max_length=50)
    total=models.CharField(max_length=100)

class mail_table(models.Model):
    email=models.CharField(max_length=150)
    subject=models.CharField(max_length=150)
    message=models.CharField(max_length=500)

class task_table(models.Model):
   course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
   batch=models.ForeignKey(batch_table,on_delete=models.CASCADE,null=True)
   teacher=models.ForeignKey(teacher_table1,on_delete=models.CASCADE,null=True)
   chapter=models.CharField(max_length=120)
   task=models.TextField(max_length=250)
   date=models.DateField(auto_now_add=True)
   due_date=models.DateField(null=True)

class task_submitted_table(models.Model):
    task=models.ForeignKey(task_table,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(student_table,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(course_table,on_delete=models.CASCADE,null=True)
    batch=models.ForeignKey(batch_table,on_delete=models.CASCADE,null=True)
    description=models.TextField(max_length=250)
    document=models.FileField(upload_to='doc/')

class feedback_table(models.Model):
    student=models.ForeignKey(student_table,on_delete=models.CASCADE,null=True)
    teacher_name=models.TextField(max_length=50)
    subject=models.TextField(max_length=50)
    feedback=models.TextField(max_length=500)
    


   


    














