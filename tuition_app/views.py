from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth,Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tuition_app.models import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime


# Create your views here.
def home(request):
    return render(request,'home.html')

def load_home(request):
    return render(request,'home.html')



def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                auth.login(request,user)
                return redirect('admin_home')
            else:
                # auth.login(request,user)
                # user_id=request.user.id
                # data=teacher_table.objects.get(user=user_id)
                # if user_id==data:
                #    return redirect('admin_home')
                # else:
                # return redirect('user_home')
                if user.groups.filter(name='student'):
                    auth.login(request,user)
                    return redirect('user_home')
                elif user.groups.filter(name='teacher'):
                    auth.login(request,user)
                    return redirect('user_home1')
              

        else:
            messages.info(request,'invalid credentials')
            return redirect('login_page')

             
@login_required(login_url='login_page')
def user_home(request):
    return render(request,'teacher/teacher_home.html')

def user_home1(request):
    return render(request,'teacher/teacher_home1.html')



def admin_home(request):
    return render(request,'administration/admin_home.html')


def add_course(request):
    if request.method=='POST':
        course_name=request.POST['course_name']
        course_fee=request.POST['course_fee']
        data=course_table(course_name=course_name,course_fee=course_fee)
        data.save()
        return redirect('admin_home')

def add_batch(request):
    if request.method=='POST':
        batch_name=request.POST['batch_name']
        data=batch_table(batch_name=batch_name)
        data.save()
        return redirect('admin_home')

def tea_signup(request):
    courses=course_table.objects.all()
    return render(request,'tea_signup.html',{"courses":courses})  

def login_page(request):
    return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['email']
        password=request.POST['password']
        address=request.POST['address']
        phone=request.POST['phone']
        image=request.FILES.get('file')
        course=request.POST['select']
        cdata=course_table.objects.get(id=course)
        x=2
        gdata=x

        if User.objects.filter(username=username).exists(): 
            messages.info(request,'this username already exists')
            return redirect('login_page')
        else:
            user=User.objects.create_user(first_name=first_name,last_name=last_name,
                                           email=email,username=username,password=password)
            user.save()
            data=User.objects.get(id=user.id)
            grp_data=user.groups.add(gdata)

            user_data=teacher_table1(address=address,phone=phone,image=image,course=cdata,user=data)
            user_data.save()
            subject = 'username and password'
            message = 'username is '+username +'password is '+password
            recipient = request.POST['email']    
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
            return redirect('login_page')

def stud_signup(request):
    batches=batch_table.objects.all()
    return render(request,'stud_signup.html',{"batches":batches})  

def student_signup(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['email']
        password=request.POST['password']
        address=request.POST['address']
        phone=request.POST['phone']
        image=request.FILES.get('file')
        batch=request.POST['select']
        bdata=batch_table.objects.get(id=batch)
        x=1
        gdata=x

        if User.objects.filter(username=username).exists(): 
            messages.info(request,'this username already exists')
            return redirect('login_page')
        else:
            user=User.objects.create_user(first_name=first_name,last_name=last_name,
                                           email=email,username=username,password=password)

            user.save()
            data=User.objects.get(id=user.id)
            grp_data=user.groups.add(gdata)
            user_data=student_table(address=address,phone=phone,image=image,batch=bdata,student=data)
            # grp_data.save()

            user_data.save()
            subject = 'username and password'
            message = 'username is '+username +'password is '+password
            recipient = request.POST['email']     #  recipient =request.POST["inputTagName"]
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
              
            return redirect('login_page')

def subject_details(request):
    course=course_table.objects.all()
    return render(request,'student/join_course.html',{'course':course})

def join_course(request,pk):
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    user1=student_table.objects.get(student=user)
    course=course_table.objects.get(id=pk)
    if tuition_table.objects.filter(course=course.id,student=user1.id).exists():
        messages.info(request,'You are already joined.......')
        return redirect("subject_details") 
    else:
        return render(request,'student/joined_course.html',{'user':user1,'course':course})


def joined_course(request,pk):
    if request.method=='POST':
        course=course_table.objects.get(id=pk)
        user1=request.user.id
        # user=User.objects.get(id=user_id)
        user2=student_table.objects.get(student=user1)
        # user3=student_table.objects.get(batch=user2.batch)
        user4=batch_table.objects.get(id=user2.batch.id)
        # stud=student.id
        data=tuition_table(student=user2,course=course)
        data.save()
        data1=tuition_table1(student=user2,course=course,batch=user4)
        data1.save()
        return redirect('user_home')

def time_table_page(request):
    batch=batch_table.objects.all()
    course=course_table.objects.all()
    teacher=teacher_table1.objects.all()
    return render(request,'administration/time_table.html',{'batch':batch,'course':course,'teacher':teacher})

def add_time_table(request):
    if request.method=='POST':
        ddata=request.POST['select1']
        batch=request.POST['select2']
        course=request.POST['select3']
        teacher=request.POST['select4']
        time_from=request.POST['time_from']
        time_to=request.POST['time_to']


        day=ddata
        batch1=batch_table.objects.get(id=batch)
        course1=course_table.objects.get(id=course)
        # teacher1=User.objects.get(id=teacher)
        teacher2=teacher_table1.objects.get(id=teacher)
        data=timetable_table(day=day,time_from=time_from,time_to=time_to,batch=batch1,course=course1,teacher=teacher2)
        data.save()
        return redirect('admin_home')

def view_timetable(request):
    user_id=request.user.id
    teacher1=User.objects.get(id=user_id)
    teacher2=teacher_table1.objects.get(user=teacher1)
    tuition=timetable_table.objects.filter(teacher=teacher2)
    return render(request,'teacher/view_timetable.html',{'tuition':tuition})
    # user_id=request.user.id


def stud_subject_list(request):
    user_id=request.user.id
    user1=User.objects.get(id=user_id)
    user2=student_table.objects.get(student=user1)
    tuition=tuition_table.objects.filter(student=user2)
    # course=course_table.objects.filter(id=tuition.course.id)
    return render(request,'student/course_list.html',{'data':tuition})

def stud_timetable(request,pk):
    user_id=request.user.id
    user1=User.objects.get(id=user_id)
    user2=student_table.objects.get(student=user1)
    tuition=tuition_table.objects.get(student=user2,id=pk)
    course=course_table.objects.get(id=tuition.course.id)
    batch=batch_table.objects.get(id=user2.batch.id)
    timetable=timetable_table.objects.filter(course=course,batch=batch)
    return render(request,'student/stud_timetable.html',{'course2':timetable})

def stud_leave_page(request):
    return render(request,'student/stud_leave.html')

def stud_leave(request):
     if request.method=='POST':
        user_id=request.user.id
        user1=User.objects.get(id=user_id)
        student=student_table.objects.get(student=user1)
        subject=request.POST['subject']
        message=request.POST['message']
        leave_date=request.POST['leave_date']
        # status=null
        data=stud_leave_table(student=student,subject=subject,message=message,leave_date=leave_date)
        data.save()
        return redirect('user_home')

def leave_list_page(request):
    data=stud_leave_table.objects.all()
    return render(request,'administration/leave_list.html',{'data':data})

def allow(request,pk):
    data=stud_leave_table.objects.get(id=pk)
    data.status="allowed"
    data.save()
    return redirect("leave_list_page")

def denay(request,pk):
    data=stud_leave_table.objects.get(id=pk)
    data.status="denied"
    data.save()
    return redirect("leave_list_page")

def stud_leave_list(request):
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    user2=student_table.objects.get(student=user)
    data=stud_leave_table.objects.filter(student=user2)
    return render(request,'student/stud_leave_list.html',{'data':data})

def tea_leave_page(request):
        return render(request,'teacher/teacher_leave.html')

def tea_leave(request):
     if request.method=='POST':
        user_id=request.user.id
        user1=User.objects.get(id=user_id)
        teacher=teacher_table1.objects.get(user=user1)
        subject=request.POST['subject']
        message=request.POST['message']
        leave_date=request.POST['leave_date']
        # status=null
        data=teacher_leave_table(teacher=teacher,subject=subject,message=message,leave_date=leave_date)
        data.save()
        return redirect('user_home')

def teacher_leave_page(request):
    data=teacher_leave_table.objects.all()
    return render(request,'administration/tea_leave_list.html',{'data':data})

def tallow(request,pk):
    data=teacher_leave_table.objects.get(id=pk)
    data.status="allowed"
    data.save()
    return redirect("teacher_leave_page")

def tdenay(request,pk):
    data=teacher_leave_table.objects.get(id=pk)
    data.status="denied"
    data.save()
    return redirect("teacher_leave_page")

def teacher_applied_leave_list(request):
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    user2=teacher_table1.objects.get(user=user)
    data=teacher_leave_table.objects.filter(teacher=user2)
    return render(request,'teacher/applied_leave_list.html',{'data':data})

def attendence_page(request,pk):
    data=timetable_table.objects.get(id=pk)
    tuition=tuition_table1.objects.filter(course=data.course,batch=data.batch)
    return render(request,'teacher/attendence.html',{'tuition':tuition})

def take_attendence_page(request,pk):
    data=tuition_table1.objects.get(id=pk)
    return render(request,'teacher/take_attendence.html',{'data':data})

def submit_attendence(request,pk):
    if request.method=='POST':
        data=tuition_table1.objects.get(id=pk)
        class_date=request.POST['class_date']
        status=request.POST['select1']
        data2=attendence(tuition=data,class_date=class_date,status=status)
        data2.save()
        return redirect('view_timetable')

def edit_attendence_page(request,pk):
    # data1=tuition_table1.objects.get(id=pk)
    data=attendence.objects.get(tuition=pk)
    return render(request,'teacher/edit_attendence.html',{'data':data})

def edit_attendence(request,pk):
    data=attendence.objects.get(id=pk)
    data.class_date=request.POST['class_date']
    data.status=request.POST['select1']
    data.save()
    return redirect("view_timetable")

def syllabus(request):
    batch=batch_table.objects.all()
    return render(request,'teacher/syllabus.html',{'batch':batch})

def add_syllabus(request):
    if request.method=='POST':
        batch=request.POST['select']
        batch1=batch_table.objects.get(id=batch)
        tea_id=request.user.id
        user1=teacher_table1.objects.get(user=tea_id)
        course=course_table.objects.get(id=user1.course.id)
        chapter=request.POST['chapter']
        topic=request.POST['topic']
        syllabus=syllabus_table(batch=batch1,course=course,teacher=user1,chapter=chapter,topic=topic)
        syllabus.save()
        return redirect('user_home')

def view_syllabus(request):
    user_id=request.user.id
    student=student_table.objects.get(student=user_id)
    tuition=tuition_table1.objects.filter(student=student)
    return render(request,'student/sub_syllabus.html',{'tuition':tuition})

def list_syllabus(request,pk):
    data=tuition_table1.objects.get(id=pk)
    data2=syllabus_table.objects.filter(course=data.course,batch=data.batch)
    return render(request,'student/list_syllabus.html',{'data2':data2})

def doc_upload_page(request):
    batch=batch_table.objects.all()
    return render(request,'teacher/doc_upload.html',{'batch':batch})

def doc_upload(request):
    if request.method=='POST':
        batch=request.POST['select']
        batch1=batch_table.objects.get(id=batch)
        tea_id=request.user.id
        user1=teacher_table1.objects.get(user=tea_id)
        course=course_table.objects.get(id=user1.course.id)
        topic=request.POST['topic']
        document=request.FILES.get('file')
        data=study_material_table(course=course,batch=batch1,teacher=user1,topic=topic,document=document)
        data.save()
        return redirect('user_home')

def list_study_material(request,pk):
    data=tuition_table1.objects.get(id=pk)
    data2=study_material_table.objects.filter(course=data.course,batch=data.batch)
    return render(request,'student/study_material_page.html',{'data2':data2})

def download_topic(request,pk):
    document=get_object_or_404(study_material_table,id=pk)
    response=HttpResponse(document.document,content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="{document.document.name}"'
    return response

def subject_mark_page(request):
    batch=batch_table.objects.all()
    return render(request,'teacher/batch_mark.html',{'batch':batch})

def student_mark(request,pk):
    batch=batch_table.objects.get(id=pk)
    user_id=request.user.id
    data1=teacher_table1.objects.get(user=user_id)
    course=course_table.objects.get(id=data1.course.id)
    tuition=tuition_table1.objects.filter(batch=batch,course=course)
    return render(request,'teacher/student_mark.html',{'tuition':tuition})

def mark_enter_page(request,pk):
    tuition=tuition_table1.objects.get(id=pk)
    return render(request,'teacher/mark_entry_page.html',{'tuition':tuition})

def submit_mark(request,pk):
    if request.method=='POST':
        teacher=request.user.id
        teacher1=teacher_table1.objects.get(user=teacher)
        tuition=tuition_table1.objects.get(id=pk)
        course=course_table.objects.get(id=tuition.course.id)
        batch=batch_table.objects.get(id=tuition.batch.id)
        student=student_table.objects.get(id=tuition.student.id)
        exam_date=request.POST['exam_date']
        exam_title=request.POST['exam_title']
        mark=request.POST['mark']
        total=request.POST['total']
        data=mark_table(course=course,batch=batch,teacher=teacher1,student=student,exam_date=exam_date,exam_title=exam_title,mark=mark,total=total)
        data.save()
        return redirect('subject_mark_page')

def stud_exam_mark(request,pk):
    # user_id=request.user.id
    # student=student_table.objects.get(student=user_id)
    data=tuition_table1.objects.get(id=pk)
    data2=mark_table.objects.filter(course=data.course,batch=data.batch,student=data.student)
    return render(request,'student/stud_exam_mark.html',{'data2':data2})

def stud_profile_page(request):
    user=request.user.id
    user1=User.objects.get(id=user)
    user1=student_table.objects.get(student=user1.id)
    return render(request,'student/stud_profile.html',{'p':user1})

def edit_stud_form(request):
    user=request.user.id
    user1=User.objects.get(id=user)
    user1=student_table.objects.get(student=user1.id)
    return render(request,'student/stud_edit_profile.html',{'p':user1})

def stud_edit_profile(request,pk):
    if request.method=='POST':
        user=student_table.objects.get(id=pk)  
        user_id=user.student.id
        user1=User.objects.get(id=user_id)
   
        if len(request.FILES)!=0:
            user.image=request.FILES['file']
           
        user1.email=request.POST.get('email')
        user.address=request.POST.get('address')
        user.phone=request.POST.get('phone')
        user1.first_name=request.POST.get('first_name')
        user1.last_name=request.POST.get('last_name')
        user.save()
        user1.save()
        return redirect('user_home')

def tea_profile_page(request):
    user=request.user.id
    user1=User.objects.get(id=user)
    user2=teacher_table1.objects.get(user=user1.id)
    return render(request,'teacher/teacher_profile.html',{'p':user2})

def edit_tea_form(request):
    user=request.user.id
    user1=User.objects.get(id=user)
    user2=teacher_table1.objects.get(user=user1.id)
    return render(request,'teacher/teacher_edit_profile.html',{'p':user2})

def teacher_edit_profile(request,pk):
    if request.method=='POST':
        user=teacher_table1.objects.get(id=pk)  
        user_id=user.user.id
        user1=User.objects.get(id=user_id)
   
        if len(request.FILES)!=0:
            user.image=request.FILES['file']
           
        user1.email=request.POST.get('email')
        user.address=request.POST.get('address')
        user.phone=request.POST.get('phone')
        user1.first_name=request.POST.get('first_name')
        user1.last_name=request.POST.get('last_name')
        user.save()
        user1.save()
        return redirect('user_home')

def teacher_list(request):
    teacher=teacher_table1.objects.all()
    return render(request,'administration/teacher_list.html',{'teacher':teacher})

def stud_batch_list(request):
    batch=batch_table.objects.all()
    return render(request,'administration/batch_student.html',{'batch':batch})

def student_list(request,pk):
    bdata=batch_table.objects.get(id=pk)
    batch=student_table.objects.filter(batch=bdata)
    return render(request,'administration/student_list.html',{'data':batch})

@login_required(login_url='login_page')
def view_more(request):
    return render(request,'student/join_course.html')

def send_mail_page(request):
    return render(request,'administration/mail.html')

def submit_mail(request):
    if request.method=='POST':
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        data=mail_table(email=email,subject=subject,message=message)
        data.save()
        subject = subject
        message = message
        recipient = request.POST['email']     #  recipient =request.POST["inputTagName"]
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
        return redirect('admin_home')
        
@login_required(login_url='login_page')
def logout(request):
    auth.logout(request)
    return redirect('home')

def add_task_page(request):
    data=batch_table.objects.all()
    return render(request,'teacher/assign_task.html',{'tuition':data})

def submit_task(request):
    if request.method=='POST':
        user_id=request.user.id
        user1=teacher_table1.objects.get(user=user_id)
        course=course_table.objects.get(id=user1.course.id)
        batch=request.POST['select']
        bdata=batch_table.objects.get(id=batch)
        chapter=request.POST['chapter']
        task=request.POST['task']
        due_date=request.POST['due_date']
        data=task_table(course=course,teacher=user1,batch=bdata,chapter=chapter,task=task,due_date=due_date)
        data.save()
        return redirect('user_home')
def task_list_page(request,pk):
    data=tuition_table1.objects.get(id=pk)
    data2=task_table.objects.filter(course=data.course,batch=data.batch)
    # data1=task_submitted_table.objects.all()  
    return render(request,'student/task_list.html',{'data2':data2})

def task_upload_page(request,pk):
    data=task_table.objects.get(id=pk)
    student=student_table.objects.get(student=request.user.id)
    if task_submitted_table.objects.filter(task=data,student=student).exists():
        messages.info(request,'you are already uploaded')
        return redirect('view_syllabus') 
    else:
        return render(request,'student/submit_task.html',{'data':data})

def task_upload(request,pk):
    if request.method=='POST':
        task=task_table.objects.get(id=pk)
        course=course_table.objects.get(id=task.course.id)
        batch=batch_table.objects.get(id=task.batch.id)
        user=request.user.id
        student=student_table.objects.get(student=user)
        description=request.POST['description']      
        document=request.FILES['file']
        task_data=task_submitted_table(task=task,student=student,course=course,batch=batch,description=description,document=document)
        task_data.save()
        return redirect(user_home)

def completed_task_list(request,pk):
    data=tuition_table1.objects.get(id=pk)
    data2=task_submitted_table.objects.filter(course=data.course,batch=data.batch,student=data.student)
    return render(request,'student/completed_task_list.html',{'data2':data2})

def task_batch_page(request):
    batch=batch_table.objects.all()
    return render(request,'teacher/task_batch.html',{'batch':batch})

def task_given_list(request,pk):
    batch=batch_table.objects.get(id=pk)
    user_id=request.user.id
    user1=User.objects.get(id=user_id)
    teacher=teacher_table1.objects.get(user=user1)
    course=course_table.objects.get(id=teacher.course.id)
    data=task_table.objects.filter(batch=batch,course=course,teacher=teacher)
    return render(request,'teacher/task_given_list.html',{'data':data})

def task_submited_students(request,pk):
    data=task_table.objects.get(id=pk)
    data1=task_submitted_table.objects.filter(task=data)
    return render(request,'teacher/task_submited_students.html',{'data1':data1})

def feedback_page(request):
    return render(request,'student/feedback.html')

def give_feedback(request):
    if request.method=='POST':
        user_id=request.user.id
        student=student_table.objects.get(student=user_id)
        teacher_name=request.POST['teacher']
        subject=request.POST['subject']
        feedback=request.POST['feedback']
        data=feedback_table(student=student,teacher_name=teacher_name,subject=subject,feedback=feedback)
        data.save()
        return redirect('user_home')

def view_feedback_page(request):
    data=feedback_table.objects.all()
    return render(request,'administration/view_feedback.html',{'data':data})

def task_sub_page(request):
    user_id=request.user.id
    student=student_table.objects.get(student=user_id)
    tuition=tuition_table1.objects.filter(student=student)
    return render(request,'student/sub_task.html',{'tuition':tuition})

def study_material_page(request):
    user_id=request.user.id
    student=student_table.objects.get(student=user_id)
    tuition=tuition_table1.objects.filter(student=student)
    return render(request,'student/sub_studymaterial.html',{'tuition':tuition})



