from django import template
from student.models import s_registration
from management.models import company as c_model

register = template.Library()

@register.filter(name='get_ctc_lac')
def get_ctc_lac(company_obj):
    value = company_obj.ctc
    if company_obj.for_batch is None:
        return str(value/100000.00)+' Lacs'
    elif company_obj.for_batch.name == 'Placement':
        value = int(value)
        value = value/100000.00
        return str(value)+' LPA.'
    elif company_obj.for_batch.name == 'Internship':
        value = int(value)
        value = value/1000.00
        return str(value)+' K /month'
    else:
        return str(value/100000.00)+' Lacs'    

@register.filter(name='get_cap_lac')
def get_cap_lac(company_obj):
    value = company_obj.cap
    if company_obj.for_batch is None:
        return str(value/100000.00)+' Lacs'
    elif company_obj.for_batch.name == 'Placement':
        value = int(value)
        value = value/100000.00
        return str(value)+' LPA.'
    elif company_obj.for_batch.name == 'Internship':
        value = int(value)
        value = value/1000.00
        return str(value)+' K /month'
    else:
        return str(value/100000.00)+' Lacs'   

@register.filter(name='get_top_placement')
def get_top_placement(user_obj):
    if  s_registration.objects.filter(user = user_obj, placed = True).count() < 1:
        return 'TNP Portal'
    t = s_registration.objects.filter(user = user_obj, placed = True).order_by('-company__ctc')[0].company.name[:12]
    return t

@register.filter(NameError='get_reg_list')
def get_reg_list(user_obj):
    l1 = s_registration.objects.filter(user = user_obj)
    l2 = []
    for l in l1:
        l2.append(l.company)
    return l2

# def placement_apply_condition_button(company_obj,usr):
#     if not company_obj.open_reg:
#         messages.error(request,"Registration Failed : Registrations for this compnay is disabled by TNP.")
#         return redirect('student:s_home')
#     if usr.student_profile.branch not in company_obj.branch_allowed.all():
#         messages.error(request,'Registration failed : Your branch is not elligible to register for this company.')
#         return redirect('student:s_home')
#     if usr.student_profile.branch.branchType.name == 'BE':
#         if usr.student_profile.be_marks < company_obj.cutoff:
#             messages.error(request,'Registration failed : You do not qualify cut off so you are not elligible to register for this company. Your BE CGPA aggr is less than cut off.')
#             return redirect('student:s_home')
#     if usr.student_profile.branch.branchType.name != 'BE':
#         if float(usr.student_profile.sem6) < company_obj.cutoff:
#             messages.error(request,
#                            'Registration failed : You do not qualify cut off so you are not elligible to register for this company. Your MTech CGPA aggr is less than cut off.')
#             return redirect('student:s_home')
#     if usr.student_profile.backlogs > company_obj.backlogs_allowed:
#         messages.error(request,'Registration failed : You have more backlogs than allowed for this company, so you are not elligible to register for this company.')
#         return redirect('student:s_home')
#     c_grade = company_obj.grade.grade
#     if s_registration.objects.filter(user = usr, placed = True, company__grade__grade__gte = c_grade).count() > 0:
#         messages.error(request,'Registration failed : You can only apply for company of higher grade than the one in which you are placed.')
#         return redirect('student:s_home')
#     c_cap = int(company_obj.cap)
#     if str(company_obj.cap)!='-1' and s_registration.objects.filter(user = usr, placed = True, company__ctc__gt = c_cap).count() > 0:
#         messages.error(request,"Registration failed : You are already placed in a company with ctc greater than "+str(c_cap))
#         return redirect('student:s_home')
