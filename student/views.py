from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import string
import datetime
from random import *
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone as django_time
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Lower
import openpyxl
from management.models import *
from student.forms import * 
from student.models import*
from management.o_f import user_creator_, user_creator_2
from management import forms as m_form
from student.generator import reg_id_generator
from student.pre_checks import ban_pre_check
from management import models as m_models

# Create your views here.

def mdc(request):
    return render(request,'mdc.html')

#views static---------------------------------------------------------------------------------------------------------
def all_home(request):
    return render(request,'all_home.html')

def alumni_s(request):
    return render(request,'alumni.html')

def courses_s(request):
    return render(request,'courses.html')

def faculty_s(request):
    return render(request,'faculty.html')

def history_s(request):
    return render(request,'history.html')

def policy_s(request):
    return render(request,'policy.html')

def procedure_s(request):
    return render(request,'procedure.html')

def students_life_s(request):
    return render(request,'students.html')

def contact_us(request):
    memberList = ['ankit agarwal','yash','lavish bansal','nikhil banka', 'amritanshu', 'tushar gahlot', 'shruti jain',
                  'dhwaj', 'tejinder', 'uzma', 'ansh', 'archit goswami', 'indranil', 'manas', 'pawan',
                  'vishnu', 'abhishek']
    memberList.sort()
    return render(request,'contact_us.html',{'memberList':memberList})

# end views static---------------------------------------------------------------------------------------------------

def student_activation(request):
    if request.user.is_authenticated():
        return redirect('/')
    form = student_activate_form()
    if request.method=='POST':
        form = student_activate_form(request.POST)
        if form.is_valid():
            roll_no = str(form.cleaned_data.get('rollno')).upper()
            if student_email_db.objects.filter(rollno = roll_no).count()==0:
                messages.error(request, "Your information doesn't exist in the database for roll no "+roll_no+"<br>Check you have filled correct roll number or Contact TNP")
                return redirect('student:s_activation') #update this please ###############################################################
            elif User.objects.filter(username = roll_no).count() < 1 and student_email_db.objects.filter(rollno = roll_no).count()>0 :
                if account_activation_check.objects.filter(roll_no = roll_no).count()<1:
                    temp_obj = account_activation_check(roll_no = roll_no, check = False, db_obj = student_email_db.objects.get(rollno = roll_no))
                    temp_obj.save()
                email = student_email_db.objects.get(rollno = roll_no).email
                user_obj = user_creator_2(roll_no,email,request)
                account_activation_check.objects.filter(roll_no = roll_no).update(check = True)
                profile_set_obj = profile_set(user = user_obj, check = False)
                profile_set_obj.save()
                messages.success(request, "Activation mail is sent to the email id you submitted to the TNP")
                return redirect('student:s_login')
            elif student_email_db.objects.filter(rollno = roll_no).count()>0 and account_activation_check.objects.filter(roll_no = roll_no).count()<1:
                temp_obj = account_activation_check(roll_no = roll_no, check = False, db_obj = student_email_db.objects.get(rollno = roll_no))
                temp_obj.save()
                email = student_email_db.objects.get(rollno = roll_no).email
                user_obj = user_creator_2(roll_no,email,request)
                account_activation_check.objects.filter(roll_no = roll_no).update(check = True)
                profile_set_obj = profile_set(user = user_obj, check = False)
                profile_set_obj.save()
                messages.success(request, "Activation mail is sent to the email id you submitted to the TNP")
                return redirect('student:s_login')
            elif account_activation_check.objects.get(roll_no = roll_no).check:
                messages.error(request,"Account for roll number "+roll_no+" is already activated. Use Forgot Password to reset the password.")
                return redirect('student:s_activation') #update this please ###############################################################
            else:
                email = student_email_db.objects.get(rollno = roll_no).email
                user_obj = user_creator_2(roll_no,email,request)
                account_activation_check.objects.filter(roll_no = roll_no).update(check = True)
                profile_set_obj = profile_set(user = user_obj, check = False)
                profile_set_obj.save()
                messages.success(request, "Activation mail is sent to the email id you submitted to the TNP")
                return redirect('student:s_login') #update this please ###############################################################
    return render(request, 's_activation.html',{'form':form})

def forgot_password(request):
    if request.user.is_authenticated():
        return redirect('/')
    form = forgot_passoword_form()
    if request.method == 'POST':
        form = forgot_passoword_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            try:
                usr = User.objects.get(username = username)
            except User.DoesNotExist:
                messages.error(request, "Either this username is not registered or not activated.")
                return redirect('student:s_forgot_pass') #update this#####################################################################
            email = usr.email
            pass_form = PasswordResetForm({'email':email})
            if pass_form.is_valid():
                pass_form.save(request=request, subject_template_name = 'password_reset_subject.txt', email_template_name='password_reset_email.html', from_email="no-reply@tnp.nsutonline.in", )
            messages.success(request, "Password Reset link is mailed to your registed ID. Check inbox and spambox.")
            return redirect('student:s_login')#update this#######################################################################
    return render(request,'s_forgot_pass.html',{'form':form})

#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr

@login_required
def s_changepass(request):
    if request.method == 'POST':
        form = m_form.PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('student:s_change_pass')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = m_form.PasswordChangeCustomForm(request.user)
    return render(request, 's_change_pass.html', {'form':form})

@login_required
@not_manager_required
@create_profile_dec
def create_profile(request):
    form = student_profile_form()
    if request.method == 'POST':
        form = student_profile_form(request.POST)
        if form.is_valid():
            db_obj = m_models.student_email_db.objects.get(rollno = request.user.username)
            finalform = form.save(commit = False)
            finalform.roll_no = request.user.username
            finalform.user = request.user
            finalform.be_marks = db_obj.cgpa
            finalform.sem1 = db_obj.sem1
            finalform.sem2 = db_obj.sem2
            finalform.sem3= db_obj.sem3
            finalform.sem4 = db_obj.sem4
            finalform.sem5 = db_obj.sem5
            finalform.sem6 = db_obj.sem6
            finalform.backlogs = db_obj.backlog
            finalform.batch = m_models.current_batch_year.objects.get(year = int(db_obj.batch))
            finalform.save()
            profile_set.objects.filter(user = request.user).update(check = True)
            return redirect('/')
    return render(request, 'create_profile.html',{'form':form})

@login_required
@not_manager_required
@is_profile_created
def student_profile_visit(request):
    form = student_profile_edit_form(instance = student_profile.objects.get(user = request.user))
    if request.method=='POST':
        form = student_profile_edit_form(request.POST, instance = student_profile.objects.get(user = request.user))
        if form.is_valid():
            form.save()
            return redirect('student:s_profile')
    return render(request, 'create_profile.html',{'form':form,'already_created':True})

@login_required
@not_manager_required
@is_profile_created
def registration_redirects(request, cid = None):
    if cid==None:
        raise Http404("No such company exists")
    cid = int(cid)
    try:
        company_obj = company.objects.get(id = cid)
    except company.DoesNotExist:
        raise Http404("No such company exists")
    if request.user.student_profile.batch.name == 'Placement':
        return redirect('student:p_reg', cid)
    if request.user.student_profile.batch.name == 'Internship':
        return redirect('student:i_reg', cid)

@login_required
@not_manager_required
@is_profile_created
def placement_registeration(request, cid = None, rid = None):
    if resume_drive.objects.filter(user=request.user).count()<1:
        messages.error(request,"Upload your resumes before applying to any company")
        return redirect('student:s_resume')
    if request.user.student_profile.batch.name == 'Internship':
        messages.error(request, "You are not elligible for registration for placements.")
        return redirect('student:s_home')
    if cid==None:
        raise Http404("No such company exists")
    cid = int(cid)
    try:
        company_obj = company.objects.get(id = cid)
    except company.DoesNotExist:
        raise Http404("No such company exists")
    usr = request.user
    if company_obj.for_batch != usr.student_profile.batch:
        messages.error(request,"Registration Failed: You can not apply for "+usr.student_profile.batch.name+" in a company asking for "+company_obj.for_batch.name+" candidates.")
        return redirect('student:s_home')
    if not company_obj.open_reg:
        messages.error(request,"Registration Failed : Registrations for this compnay is disabled by TNP.")
        return redirect('student:s_home')
    if usr.student_profile.branch not in company_obj.branch_allowed.all():
        messages.error(request,'Registration failed : Your branch is not elligible to register for this company.')
        return redirect('student:s_home')
    if usr.student_profile.branch.branchType.name == 'BE':
        if usr.student_profile.be_marks < company_obj.cutoff:
            messages.error(request,'Registration failed : You do not qualify cut off so you are not elligible to register for this company. Your BE CGPA aggr is less than cut off.')
            return redirect('student:s_home')
    if usr.student_profile.branch.branchType.name != 'BE':
        if float(usr.student_profile.sem6) < company_obj.cutoff:
            messages.error(request,
                           'Registration failed : You do not qualify cut off so you are not elligible to register for this company. Your MTech CGPA aggr is less than cut off.')
            return redirect('student:s_home')
    if usr.student_profile.backlogs > company_obj.backlogs_allowed:
        messages.error(request,'Registration failed : You have more backlogs than allowed for this company, so you are not elligible to register for this company.')
        return redirect('student:s_home')
    c_grade = company_obj.grade.grade
    if s_registration.objects.filter(user = usr, placed = True, company__grade__grade__gte = c_grade).count() > 0:
        messages.error(request,'Registration failed : You can only apply for company of higher grade than the one in which you are placed.')
        return redirect('student:s_home')
    c_cap = int(company_obj.cap)
    if str(company_obj.cap)!='-1' and s_registration.objects.filter(user = usr, placed = True, company__ctc__gt = c_cap).count() > 0:
        messages.error(request,"Registration failed : You are already placed in a company with ctc greater than "+str(c_cap))
        return redirect('student:s_home')
    date = django_time.localdate()
    if date > company_obj.closing_date:
        messages.error(request,'Registration failed : Registration for this company have been closed.')
        return redirect('student:s_home')
    if s_registration.objects.filter(user = usr,company = company_obj ).count()>0:
        messages.error(request, "You are already registerd for "+company_obj.name+" with registration number "+str(s_registration.objects.filter(user = usr,company = company_obj )[0].reg_id))
        return redirect('student:s_home')
    ban_status, ban_statement = ban_pre_check(request.user,company_obj)
    if ban_status:
        messages.error(request,"Registration Failed : "+ban_statement)
        return redirect('student:s_home')
    if rid==None:
        return render(request,'select_resume.html',{'cid':cid,'usr':request.user})
    rid = int(rid)
    if rid==1:
        r_path = 1
    elif rid==2:
        print(request.user.resume_drive.resume2)
        if request.user.resume_drive.resume2 == '':
            messages.error(request,'Registration failed : You have selected second resume to be used with application for '+company_obj.name+'. But you have not uploaded any second resume. Try Again !')
            return redirect('student:s_home')
        r_path = 2
    elif rid ==3:
        if request.user.resume_drive.resume3 == '':
            messages.error(request,'Registration failed : You have selected third resume to be used with application for '+company_obj.name+'. But you have not uploaded any third resume. Try Again !')
            return redirect('student:s_home')
        r_path = 3
    elif rid>3:
        raise Http404("Invalid Request")
    reg_obj = s_registration(user = usr, company = company_obj, r_file = r_path, reg_type = company_obj.for_batch)
    reg_obj.save()
    messages.success(request, "You have successfully registered for "+company_obj.name)
    return redirect('student:s_home')

@login_required
@not_manager_required
@is_profile_created
def internship_registeration(request, cid = None, rid = None):
    if resume_drive.objects.filter(user=request.user).count()<1:
        messages.error(request,"Upload your resumes before applying to any company")
        return redirect('student:s_resume')
    if request.user.student_profile.batch.name == 'Placement':
        messages.error(request, "You are not elligible for registration for internships.")
        return redirect('student:s_home')
    if cid==None:
        raise Http404("No such company exists")
    cid = int(cid)
    try:
        company_obj = company.objects.get(id = cid)
    except company.DoesNotExist:
        raise Http404("No such company exists")
    usr = request.user
    if company_obj.for_batch != usr.student_profile.batch:
        messages.error(request,"Registration Failed: You can not apply for "+usr.student_profile.batch.name+" in a company asking for "+company_obj.for_batch.name+" candidates.")
        return redirect('student:s_home')
    if not company_obj.open_reg:
        messages.error(request,"Registration Failed : Registrations for this compnay is disabled by TNP.")
        return redirect('student:s_home')
    if usr.student_profile.branch not in company_obj.branch_allowed.all():
        messages.error(request,'Registration failed : Your branch is not elligible to register for this company.')
        return redirect('student:s_home')
    if usr.student_profile.branch.branchType.name == 'BE':
        if usr.student_profile.be_marks < company_obj.cutoff:
            messages.error(request,'Registration failed : You do not qualify cut off so you are not elligible to register for this company. Your BE CGPA aggr is less than cut off.')
            return redirect('student:s_home')
    if usr.student_profile.branch.branchType.name != 'BE':
        if float(usr.student_profile.sem6) < company_obj.cutoff:
            messages.error(request,
                           'Registration failed : You do not qualify cut off so you are not elligible to register for this company. Your MTech CGPA aggr is less than cut off.')
            return redirect('student:s_home')
    if usr.student_profile.backlogs > company_obj.backlogs_allowed:
        messages.error(request,'Registration failed : You have more backlogs than allowed for this company, so you are not elligible to register for this company.')
        return redirect('student:s_home')
    c_grade = company_obj.grade.grade
    if s_registration.objects.filter(user = usr, placed = True).count() > 0 and str(company_obj.cap)=='-1':
        messages.error(request,'Registration failed : You can not apply for more internships if already placed in atleast one internship.')
        return redirect('student:s_home')
    c_cap = int(company_obj.cap)
    if str(company_obj.cap)!='-1' and s_registration.objects.filter(user = usr, placed = True, company__ctc__gt = c_cap).count() > 0:
        messages.error(request,"Registration failed : You are already placed for internship in a company with ctc greater than "+str(c_cap))
        return redirect('student:s_home')
    date = django_time.localdate()
    if date > company_obj.closing_date:
        messages.error(request,'Registration failed : Registration for this company have been closed.')
        return redirect('student:s_home')
    if s_registration.objects.filter(user = usr,company = company_obj ).count()>0:
        messages.error(request, "You are already registerd for "+company_obj.name+" with registration number "+str(s_registration.objects.filter(user = usr,company = company_obj )[0].reg_id))
        return redirect('student:s_home')
    ban_status, ban_statement = ban_pre_check(request.user,company_obj)
    if ban_status:
        messages.error(request,"Registration Failed : "+ban_statement)
        return redirect('student:s_home')
    if rid==None:
        return render(request,'select_resume.html',{'cid':cid,'usr':request.user})
    rid = int(rid)
    if rid==1:
        r_path = 1
    elif rid==2:
        print(request.user.resume_drive.resume2)
        if request.user.resume_drive.resume2 == '':
            messages.error(request,'Registration failed : You have selected second resume to be used with application for '+company_obj.name+'. But you have not uploaded any second resume. Try Again !')
            return redirect('student:s_home')
        r_path = 2
    elif rid ==3:
        if request.user.resume_drive.resume3 == '':
            messages.error(request,'Registration failed : You have selected third resume to be used with application for '+company_obj.name+'. But you have not uploaded any third resume. Try Again !')
            return redirect('student:s_home')
        r_path = 3
    elif rid>3:
        raise Http404("Invalid Request")
    reg_obj = s_registration(user = usr, company = company_obj, r_file = r_path, reg_type = company_obj.for_batch)
    reg_obj.save()
    messages.success(request, "You have successfully registered for "+company_obj.name)
    return redirect('student:s_home')


@login_required
@not_manager_required
@is_profile_created
def s_home(request,slug = None):
    name_order = ''
    cut_off_order = ''
    last_date_order = ''
    form = home_search_form()
    if request.method == 'POST':
        form = home_search_form(request.POST)
        if form.is_valid():
            str1 = form.cleaned_data.get('slug')
            return redirect('student:s_home_search', slug=str1)
    if slug==None:
        c_list = company.objects.all()
    else:
        slug = str(slug)
        try:
            br = str(slug)
            br = br.upper()
            c_list  = company.objects.filter(branch_allowed__name__icontains = br)
            if c_list:
                messages.success(request, "Search results for company allowing branch "+str(slug)+" :")
        except company.DoesNotExist:
            c_list = None
        if not c_list:
            try:
                c_list = company.objects.filter(name__icontains = slug)
                if c_list:
                    messages.success(request, "Search results for company name containing "+str(slug)+" :")
            except company.DoesNotExist:
                c_list = None
    if request.GET.get('orderby'):
        o = str(request.GET.get('orderby'))
        
        if o=='cutoff':
            c_list=c_list.order_by('cutoff')
            cut_off_order = 'active'
        elif o=='lastdate':
            c_list=c_list.order_by('closing_date')
            last_date_order = 'active'
        else: 
            c_list = c_list.order_by(Lower('name'))
            name_order = 'active'
    else:
        c_list=c_list.order_by(Lower('name'))
        name_order = 'active'
    date = django_time.localdate()
    c_list = c_list.filter(closing_date__gte = date)
    b_q = False
   
    arg = {
        'clist':c_list.filter(for_batch = request.user.student_profile.batch),
        'name_order':name_order,
        'cut_off_order':cut_off_order,
        'last_date_order':last_date_order,
        'date':date,
        'branch_qualification': b_q,
        'zero':0
        }
    return render(request, 's_home.html',arg)

@login_required
@not_manager_required
@is_profile_created
def my_reg_list(request):
    reg_list = s_registration.objects.filter(user = request.user)
    return render(request,'my_reg_list.html',{'rlist':reg_list})

@login_required
@not_manager_required
@is_profile_created
def delete_registration(request, reg_id=None):
    try:
        reg_id = int(reg_id)
    except:
        raise Http404
    if s_registration.objects.filter(reg_id=reg_id).count()<1:
        messages.error(request,"No such application found")
    else:
        r_obj = s_registration.objects.get(reg_id=reg_id)
        date = django_time.localdate()

        if r_obj.placed:
            messages.error(request,"You can not delete application after being placed in that company.")
        elif not r_obj.company.open_reg:
            messages.error(request,"You can not cancel registration if registrations for a company are suspended and registrations for "+r_obj.company.name+" are suspended.")
        elif date > r_obj.company.closing_date:
            messages.error(request,"You can not cancel registration after registrations for a company are closed.")
        else:
            s_registration.objects.filter(reg_id=reg_id).delete()
            messages.success(request,"Cancelled Successfully")
    return redirect('student:my_reg')

@login_required
@not_manager_required
@is_profile_created
def resume_management_student(request):
    if resume_drive.objects.filter(user=request.user).count()>0:
        form = resume_drive_form(instance=resume_drive.objects.get(user=request.user))
    else:
        form = resume_drive_form()
    if request.method=='POST':
        if resume_drive.objects.filter(user=request.user).count()>0:
            form = resume_drive_form(request.POST, request.FILES, instance=resume_drive.objects.get(user=request.user))
        else: 
            form = resume_drive_form(request.POST, request.FILES)
        if form.is_valid():
            if resume_drive.objects.filter(user=request.user).count()>0:
                form.save()
            else:
                finalform = form.save(commit=False)
                finalform.user=request.user
                finalform.save()
            return redirect('student:s_resume')
    return render(request, 's_resume_management.html',{'form':form})